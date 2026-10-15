# HyperFrames + Whisper

Personal desktop plugin with 21 upstream HyperFrames skills and three added workflows: whisper-transcription, video-library and video-script-planner.

## Usage
- Create a 30-second explainer from my script.
- Transcribe this recording in its original language and export TXT, SRT and VTT.
- Find videos in this project and summarize those with existing transcripts.

## Requirements
Node.js 22+ with npm, FFmpeg, a desktop agent with shell and file access, and internet for initial CLI/model downloads. The upstream CLI is pinned to 0.8.162. This is a skills package, not a hosted MCP service. It does not access your HeyGen/Tella cloud library. Cloud media generation or publishing requires separately configured providers and authorization. Speech models are not included. First transcription will verify runtime support and download its model.

## Attribution
HyperFrames skills from HeyGen, commit a403ea1e8b283c6bdcbe21b5cab2a2a50b5f35f3, licensed under Apache-2.0. See LICENSE and NOTICE. Personal customizations are not an official HeyGen or OpenAI product.
