---
name: video-library
description: Find, inventory, summarize and organize existing local video projects, rendered videos and their transcripts. Use when the user asks to manage or search their video library.
---

# Local video library

Scope searches to the workspace or folder provided by the user. If unspecified, use the current workspace and state that scope. This plugin does not connect to the user's HeyGen or Tella cloud account.

Use `rg --files` to find video extensions (mp4, mov, mkv, webm, avi), hyperframes.json, BRIEF.md, STORYBOARD.md and transcript files. Record absolute path, size and modification time. Use ffprobe with argument arrays and JSON output for duration, dimensions and audio tracks. Report per-file failures; do not mistake an unsupported file for an empty library. Do not traverse unrelated user folders.

Return a compact inventory with clickable paths. Search existing TXT/JSON/SRT/VTT transcripts for content questions; filenames alone do not establish what a video contains. If transcription is needed, invoke ../whisper-transcription/SKILL.md on the selected files. For script planning load ../video-script-planner/SKILL.md; for editing or rendering an existing project load ../hyperframes/SKILL.md.

When organization is requested, create an index in the user's project with source paths and links to derived outputs. Preserve originals. Rename, move or delete media only within the user's explicit requested scope, checking collisions first. Do not upload or publish media merely because it was indexed.
