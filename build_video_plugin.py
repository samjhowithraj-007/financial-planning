from pathlib import Path
import json, shutil, subprocess, zipfile, yaml

base = Path(__file__).resolve().parent
upstream = base / 'hyperframes-upstream'
root = base / 'hyperframes-whisper'
root.mkdir(exist_ok=True)
shutil.copytree(upstream / 'skills', root / 'skills', dirs_exist_ok=True)
shutil.copy2(upstream / 'LICENSE', root / 'LICENSE')
version = json.loads((upstream / 'plugin.json').read_text())['version']
commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=upstream, text=True).strip()

def write(path, text):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')

manifest = {
 '$schema': 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
 'name': 'hyperframes-whisper', 'version': '0.1.0',
 'description': 'Personal HyperFrames video creation, script planning, local video library and Whisper transcription workflows.',
 'author': {'name': 'Personal workspace'}, 'license': 'Apache-2.0',
 'extensions': {'com.openai': {'interface': {
 'displayName': 'HyperFrames + Whisper', 'shortDescription': 'Videos, scripts & transcripts',
 'longDescription': 'Create and edit videos with bundled HyperFrames skills, plan scripts, find local videos, and transcribe audio or video with local Whisper. Requires a desktop coding runtime, Node.js 22+ and FFmpeg. Runtime and speech models download on first use. No HeyGen account library connection is included. Personal customization, not an official HeyGen or OpenAI product.',
 'developerName': 'Personal workspace', 'category': 'Productivity', 'capabilities': [],
 'logo': './assets/logo.svg', 'logoDark': './assets/logo-dark.svg',
 'composerIcon': './assets/logo.svg', 'composerIconDark': './assets/logo-dark.svg',
 'brandColor': '#7C3AED', 'brandColorDark': '#C4B5FD',
 'defaultPrompt': ['Create a video from my script.', 'Transcribe my video and export subtitles.', 'Find and summarize videos in my project folder.']
 }}, 'dev.personal.hyperframes': {'cliVersion': version, 'sourceCommit': commit}}
}
write('plugin.json', json.dumps(manifest, indent=2) + '\n')
for filename, bg, fg in [('logo.svg', '#7C3AED', '#FFFFFF'), ('logo-dark.svg', '#C4B5FD', '#21103C')]:
    write('assets/' + filename, f'<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128"><rect width="128" height="128" rx="28" fill="{bg}"/><path d="M30 30 L30 98 L77 64 Z" fill="{fg}"/><g stroke="{fg}" stroke-width="6" stroke-linecap="round"><path d="M86 48 V80"/><path d="M99 38 V90"/></g></svg>')
write('NOTICE', f'Includes HyperFrames skills by HeyGen, Apache-2.0.\nSource: https://github.com/heygen-com/hyperframes\nCommit: {commit}\nCLI release: {version}\nPersonal modifications: plugin identity, launcher manifest lookup, transcription, library and planning skills, export helper and icons.\nWhisper runtime and model weights are downloaded separately, not distributed in this archive.\n')
launcher = root / 'skills/hyperframes/scripts/plugin-cli.mjs'
text = launcher.read_text(encoding='utf-8').replace('manifest.name !== "hyperframes"', 'manifest.name !== "hyperframes-whisper"')
text = text.replace('const manifest = JSON.parse(readFileSync(file, "utf8"));', 'const manifest = JSON.parse(readFileSync(file, "utf8"));\n    // Personal bundle: pin upstream CLI separately from bundle version.\n    manifest.version = manifest.extensions?.["dev.personal.hyperframes"]?.cliVersion;')
launcher.write_text(text, encoding='utf-8')
rules = root / 'skills/hyperframes/references/plugin-installation.md'
rules.write_text(rules.read_text(encoding='utf-8').replace('identifying `hyperframes`', 'identifying `hyperframes-whisper`').replace("selects the manifest's CLI version", "selects the pinned CLI version in extensions.dev.personal.hyperframes.cliVersion"), encoding='utf-8')

write('skills/whisper-transcription/SKILL.md', '''---
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
''')
write('skills/video-library/SKILL.md', '''---
name: video-library
description: Find, inventory, summarize and organize existing local video projects, rendered videos and their transcripts. Use when the user asks to manage or search their video library.
---

# Local video library

Scope searches to the workspace or folder provided by the user. If unspecified, use the current workspace and state that scope. This plugin does not connect to the user's HeyGen or Tella cloud account.

Use `rg --files` to find video extensions (mp4, mov, mkv, webm, avi), hyperframes.json, BRIEF.md, STORYBOARD.md and transcript files. Record absolute path, size and modification time. Use ffprobe with argument arrays and JSON output for duration, dimensions and audio tracks. Report per-file failures; do not mistake an unsupported file for an empty library. Do not traverse unrelated user folders.

Return a compact inventory with clickable paths. Search existing TXT/JSON/SRT/VTT transcripts for content questions; filenames alone do not establish what a video contains. If transcription is needed, invoke ../whisper-transcription/SKILL.md on the selected files. For script planning load ../video-script-planner/SKILL.md; for editing or rendering an existing project load ../hyperframes/SKILL.md.

When organization is requested, create an index in the user's project with source paths and links to derived outputs. Preserve originals. Rename, move or delete media only within the user's explicit requested scope, checking collisions first. Do not upload or publish media merely because it was indexed.
''')
write('skills/video-script-planner/SKILL.md', '''---
name: video-script-planner
description: Write or revise video scripts, hooks, narration, scene outlines and shot plans before HyperFrames production. Use for video ideas, scriptwriting, planning or converting a transcript into a video brief.
---

# Script and storyboard

Use the user's subject, audience, duration, language, platform and provided source material. Reuse established preferences. If the subject is missing, ask one concise question; otherwise draft with stated assumptions. Match language and tone to the audience.

Deliver a hook, a complete narration script, and a scene table with time range, spoken text, visual idea and on-screen text. Keep narration plausible for the duration, avoid unsupported factual claims, and distinguish supplied facts from suggested creative material. For a source recording read its transcript first, using ../whisper-transcription/SKILL.md when needed.

Save the script and storyboard in the user project when requested or needed for production. A script-only request ends with the script. If video creation was requested, continue through ../hyperframes/SKILL.md, carrying forward the completed brief rather than repeating questions. Use ../hyperframes-creative/SKILL.md for visual direction and ../hyperframes-core/SKILL.md for composition constraints. Render and inspect outputs before claiming the video is complete.
''')
write('README.md', f'''# HyperFrames + Whisper

Personal desktop plugin with 21 upstream HyperFrames skills and three added workflows: whisper-transcription, video-library and video-script-planner.

## Usage
- Create a 30-second explainer from my script.
- Transcribe this recording in its original language and export TXT, SRT and VTT.
- Find videos in this project and summarize those with existing transcripts.

## Requirements
Node.js 22+ with npm, FFmpeg, a desktop agent with shell and file access, and internet for initial CLI/model downloads. The upstream CLI is pinned to {version}. This is a skills package, not a hosted MCP service. It does not access your HeyGen/Tella cloud library. Cloud media generation or publishing requires separately configured providers and authorization. Speech models are not included. First transcription will verify runtime support and download its model.

## Attribution
HyperFrames skills from HeyGen, commit {commit}, licensed under Apache-2.0. See LICENSE and NOTICE. Personal customizations are not an official HeyGen or OpenAI product.
''')
print(f'Prepared {root}; upstream {version} at {commit}')
write('skills/whisper-transcription/scripts/export-transcript.mjs', (base / 'transcript-export-template.mjs').read_text(encoding='utf-8'))

# Validate parsed manifests, skill metadata, agent metadata and archive contents.
names = set()
for skill in sorted((root / 'skills').glob('*/SKILL.md')):
    content = skill.read_text(encoding='utf-8')
    metadata = yaml.safe_load(content.split('---', 2)[1])
    assert metadata['name'] == skill.parent.name, skill
    assert isinstance(metadata['description'], str) and metadata['description'].strip(), skill
    assert metadata['name'] not in names
    names.add(metadata['name'])
for agent in (root / 'skills').rglob('openai.yaml'):
    assert isinstance(yaml.safe_load(agent.read_text(encoding='utf-8')), dict)
assert len(manifest['extensions']['com.openai']['interface']['shortDescription']) <= 30
archive = base / 'hyperframes-whisper.zip'
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for file in sorted(root.rglob('*')):
        if file.is_file():
            assert not file.is_symlink()
            z.write(file, file.relative_to(base).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    packaged = json.loads(z.read('hyperframes-whisper/plugin.json'))
    assert packaged == manifest
    assert sum(p.endswith('/SKILL.md') and p.count('/') == 3 for p in z.namelist()) == len(names)
assert archive.stat().st_size < 100_000_000
print(f'Validated {len(names)} skills; ZIP {archive.stat().st_size} bytes: {archive}')

