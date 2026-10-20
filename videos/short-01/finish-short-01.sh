#!/usr/bin/env bash
# Paisa Samjho 1: render yt + ig, mix the clean voice (already -15 LUFS, fixed gain) with the ducked Every Dawn bed.
set -u
cd "$(dirname "$0")"
TAG="${TAG:-}"
OUT="/c/Users/rajpr/Videos/YouTube Renders/paisa-samjho-01"
BED="../_shared/music/every-dawn-loop10.mp3"
mkdir -p short/renders "$OUT"
for PL in yt ig; do
  PYTHONUTF8=1 python build-short-01.py $PL > /dev/null
  (cd short && npx --yes hyperframes@0.8.154 render . --resolution 1080p --video-bitrate 14M --workers 2 -o renders/raw-$PL.mp4 > render-$PL.log 2>&1) || { echo "RENDER FAIL $PL"; tail -5 short/render-$PL.log; exit 1; }
  FO=$(python -c "import subprocess;d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','short/renders/raw-$PL.mp4']));print(max(0,d-2.5))")
  ffmpeg -y -v error -i short/renders/raw-$PL.mp4 -i short/assets/voice.m4a -stream_loop -1 -i "$BED" -filter_complex \
   "[1:a]aresample=48000,apad,asplit=2[voice][sc];[2:a]volume=-19dB,afade=t=in:d=1[bed];[bed][sc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[duck];[voice][duck]amix=inputs=2:duration=longest:normalize=0,atrim=0:$(python -c "print($FO+2.5)"),afade=t=out:st=$FO:d=2.5,alimiter=limit=0.89[a]" \
   -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 256k -shortest -color_primaries bt709 -color_trc bt709 -colorspace bt709 -color_range tv \
   -movflags +write_colr+faststart short/renders/paisa-samjho-01${TAG}-$PL.mp4
  echo "$PL: $(ffprobe -v error -show_entries format=duration -of csv=p=0 short/renders/paisa-samjho-01${TAG}-$PL.mp4)s"
  cp short/renders/paisa-samjho-01${TAG}-$PL.mp4 "$OUT/"
done
cp thumbnail/cover-1080x1920.png "$OUT/paisa-samjho-01${TAG}-cover.png"
ls -la "$OUT"
echo SHORT DONE
