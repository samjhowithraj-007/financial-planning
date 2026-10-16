#!/usr/bin/env bash
# Part 1 Short: wait for the long render, then render yt + ig, mix voice + ducked bed, deliver.
set -u
cd "$(dirname "$0")"
OUT="/c/Users/rajpr/Videos/YouTube Renders/money-plan-01"
BED="../_shared/music/every-dawn-loop10.mp3"
log(){ echo "[$(date +%H:%M:%S)] $*"; }
log "waiting for the long video to finish"
until grep -q "ALL DONE\|RENDER FAILED TWICE" finish.log 2>/dev/null; do sleep 30; done
mkdir -p short/renders
for PL in yt ig; do
  log "build + render $PL"
  PYTHONUTF8=1 python build-short.py $PL > /dev/null
  (cd short && npx --yes hyperframes@0.8.154 render . --resolution 1080p --video-bitrate 14M --workers 2 -o renders/raw-$PL.mp4 > render-$PL.log 2>&1) || { log "RENDER FAIL $PL"; tail -5 short/render-$PL.log; exit 1; }
  FO=$(python -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','short/renders/raw-$PL.mp4']));print(max(0,d-2.5))")
  ffmpeg -y -v error -i short/renders/raw-$PL.mp4 -stream_loop -1 -i "$BED" -filter_complex \
   "[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,asplit=2[voice][sc];[1:a]volume=-17dB,afade=t=in:d=1[bed];[bed][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];[voice][duck]amix=inputs=2:duration=first:normalize=0,afade=t=out:st=$FO:d=2.5,alimiter=limit=0.89[a]" \
   -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
   -movflags +write_colr+faststart short/renders/money-plan-01-short-$PL.mp4
  log "$PL: $(ffprobe -v error -show_entries format=duration -of csv=p=0 short/renders/money-plan-01-short-$PL.mp4)s"
  cp short/renders/money-plan-01-short-$PL.mp4 "$OUT/"
done
cp thumbnail/cover-1080x1920.png "$OUT/money-plan-01-short-cover.png"
ls -la "$OUT"
log "SHORT DONE"
