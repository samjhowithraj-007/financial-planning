---
name: whisper-transcription
description: Transcribe audio or video with local Whisper, preserve the spoken language, and export TXT, SRT and VTT subtitles. Use for transcription, speech to text, captions, transcript summaries or searchable video content.
---

# Transcribe with Whisper

Read ../hyperframes/references/plugin-installation.md and ../media-use/audio/references/transcribe.md. All CLI examples below run through the pinned plugin launcher, from a user project directory, with absolute input paths. This uses local Whisper through HyperFrames; it is not an account connection to a third-party service named WhisperAI.

1. Resolve the input file and a new output directory in the user's workspace. For a URL, use only an available authorized download mechanism; do not claim a URL was read without accessing the media. Check Node.js 22+ and FFmpeg. Run the launcher with `transcribe --help` before relying on flags. First use downloads the CLI and model; report setup failures accurately.
2. Run `node "<PLUGIN_ROOT>/skills/hyperframes/scripts/plugin-cli.mjs" transcribe "<absolute-media-path>" --engine whisper --model small --dir "<new-output-directory>"`. Use the multilingual model by default; pass a language only when established by the user or verified audio. Do not silently translate. Never send audio to a remote provider without user authorization. If the platform cannot run the local engine, report the dependency/platform error and preserve the source.
3. Inspect generated transcript.json. Read the complete transcript and the bundled caption quality reference. Do not invent missing speech or speaker identities. Preserve the raw result, mark uncertain passages separately, and distinguish summaries or corrections from verbatim transcription.
4. Export using `node "<PLUGIN_ROOT>/skills/whisper-transcription/scripts/export-transcript.mjs" "<transcript.json>" "<new-export-directory>"`. The helper accepts HyperFrames flat word arrays and writes TXT, SRT and VTT, refusing to overwrite files. These captions group word timestamps into readable cues; review cue breaks and timing against the media before final delivery.
5. If requested, summarize from the transcript with timestamped takeaways. For burned-in captions route to ../embedded-captions/SKILL.md. Link the real outputs and state any unverified transcription sections. Whisper does not establish speaker identity or guarantee diarization.
