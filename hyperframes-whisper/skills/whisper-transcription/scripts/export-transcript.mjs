import { readFileSync, mkdirSync, existsSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { pathToFileURL } from 'node:url';

export function makeExports(words) {
  if (!Array.isArray(words) || !words.length) throw new Error('Expected a nonempty HyperFrames word array.');
  let previous = -1;
  for (const w of words) {
    if (typeof w.text !== 'string' || !w.text.trim() || !Number.isFinite(w.start) || !Number.isFinite(w.end) || w.start < 0 || w.end < w.start || w.start < previous) throw new Error('Invalid or unsorted word timestamp.');
    previous = w.start;
  }
  const cues = [];
  let group = [];
  const flush = () => { if (group.length) cues.push({start:group[0].start, end:group.at(-1).end, text:group.map(w=>w.text.trim()).join(' ')}); group=[]; };
  for (const w of words) {
    if (group.length && (w.start-group.at(-1).end > 1 || w.end-group[0].start > 5 || [...group, w].map(x=>x.text.trim()).join(' ').length > 72)) flush();
    group.push(w);
    if (/[.!?。！？]$/.test(w.text.trim())) flush();
  }
  flush();
  const stamp = (seconds, sep) => {
    const total = Math.round(seconds*1000);
    return `${String(Math.floor(total/3600000)).padStart(2,'0')}:${String(Math.floor(total/60000)%60).padStart(2,'0')}:${String(Math.floor(total/1000)%60).padStart(2,'0')}${sep}${String(total%1000).padStart(3,'0')}`;
  };
  const body = sep => cues.map((c,i)=>`${i+1}\n${stamp(c.start,sep)} --> ${stamp(Math.max(c.end,c.start+0.001),sep)}\n${c.text.replace(/[\r\n]+/g,' ')}\n`).join('\n');
  return {txt: words.map(w=>w.text.trim()).join(' ')+'\n', srt:body(','), vtt:'WEBVTT\n\n'+body('.')};
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [input, output] = process.argv.slice(2);
    if (!input || !output) throw new Error('Usage: node export-transcript.mjs transcript.json new-output-directory');
    const results = makeExports(JSON.parse(readFileSync(input, 'utf8')));
    const targets = Object.keys(results).map(ext=>join(output,`transcript.${ext}`));
    if (targets.some(existsSync)) throw new Error('Output exists; choose a new export directory.');
    mkdirSync(output,{recursive:true});
    for (const [ext,text] of Object.entries(results)) writeFileSync(join(output,`transcript.${ext}`),text,{encoding:'utf8',flag:'wx'});
    console.log(JSON.stringify({files:targets}));
  } catch (err) {console.error(err.message); process.exitCode=1;}
}
