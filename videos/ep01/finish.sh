#!/usr/bin/env bash
# Part 1 long video, unattended: render -> BT.709 tags -> voice level + ducked lo-fi bed -> checks -> delivery -> push.
# Usage (from videos/ep01): bash finish.sh   (log: finish.log)
set -u
cd "$(dirname "$0")"
SK="$HOME/.claude/skills/youtube-edit/scripts"
OUT="/c/Users/rajpr/Videos/YouTube Renders/money-plan-01"
BED="/c/samjhowithraj/vlog1/videos/_shared/music/all-of-the-things.mp3"
mkdir -p renders "$OUT"
log(){ echo "[$(date +%H:%M:%S)] $*"; }

log "render start (1080p, segmented, 1 worker)"
rm -rf "$TEMP"/hyperframes-extract-cache-* 2>/dev/null
PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS=3600 HF_SEGMENTED_CAPTURE=true HF_SEGMENT_FRAMES=1500 HF_SEGMENT_BROWSER_RECYCLE=1 \
  npx --yes hyperframes@0.8.154 render draft --resolution 1080p --video-bitrate 16M --workers 1 \
  -o renders/money-plan-01-raw.mp4 > render-final.log 2>&1 \
  || { log "RENDER FAILED, retrying with --resume"; PRODUCER_STREAMING_ENCODE_MAX_DURATION_SECONDS=3600 HF_SEGMENTED_CAPTURE=true \
       HF_SEGMENT_FRAMES=1500 HF_SEGMENT_BROWSER_RECYCLE=1 npx --yes hyperframes@0.8.154 render draft --resolution 1080p \
       --video-bitrate 16M --workers 1 --resume -o renders/money-plan-01-raw.mp4 >> render-final.log 2>&1 || { log "RENDER FAILED TWICE"; exit 1; }; }
log "render done: $(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/money-plan-01-raw.mp4)s"

log "BT.709 tags"
ffmpeg -y -v error -i renders/money-plan-01-raw.mp4 -c copy -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -color_range tv -movflags +write_colr+faststart renders/money-plan-01-tagged.mp4

log "append the series outro (tracker walkthrough + subscribe/follow)"
OUTRO="../_shared/outro/outro.mp4"
ffmpeg -y -v error -i renders/money-plan-01-tagged.mp4 -i "$OUTRO" -filter_complex  "[0:v]fps=30,format=yuv420p[v0];[1:v]fps=30,format=yuv420p[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]"  -map "[v]" -map "[a]" -c:v libx264 -crf 16 -preset fast -g 30 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709  -color_range tv -c:a aac -b:a 256k -movflags +write_colr+faststart renders/money-plan-01-joined.mp4
log "voice to -15 LUFS, lo-fi bed ducked under it"
END=$(ffprobe -v error -show_entries format=duration -of csv=p=0 renders/money-plan-01-joined.mp4)
FO=$(python -c "print(max(0,$END-2.5))")
ffmpeg -y -v error -i renders/money-plan-01-joined.mp4 -stream_loop -1 -i "$BED" -filter_complex \
 "[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,asplit=2[voice][sc];[1:a]volume=-17dB,afade=t=in:d=1[bed];[bed][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];[voice][duck]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=$FO:d=2.5,alimiter=limit=0.89[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest -movflags +faststart renders/money-plan-01-yt.mp4

log "checks"
PYTHONUTF8=1 python "$SK/verify-render.py" --render renders/money-plan-01-yt.mp4 --res 1920x1080 --out renders/verify > verify.log 2>&1
grep -E "PASS|FAIL|skip" verify.log | tail -8
ffmpeg -i renders/money-plan-01-yt.mp4 -af ebur128 -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
ffmpeg -v error -i renders/money-plan-01-yt.mp4 -vf "select='not(mod(n\,900))',scale=480:270,tile=6x3" -frames:v 1 -y renders/final-sheet.png

log "deliver"
cp renders/money-plan-01-yt.mp4 renders/final-sheet.png "$OUT/"
md5sum renders/money-plan-01-yt.mp4 "$OUT/money-plan-01-yt.mp4"

log "save project"
cd "/c/samjhowithraj/financial planning" && git add -A && git commit -q -m "Part 1 long video v2: captions above Raj, taller screen, 2 s section cards, subscribe + follow end screen, clean scenes, full-width labels, tracker walkthrough outro

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && GIT_TERMINAL_PROMPT=0 git push -q 2>&1 | tail -1
log "ALL DONE"
