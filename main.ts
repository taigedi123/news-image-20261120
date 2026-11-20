// Entry point for the news-image-20261120 entry.
//
// The front page itself is drawn by draw.py (run it first to regenerate
// entry.png from code). This script only drops a copy of entry.png into
// the directory the grader expects, so the submitted image is exactly the
// file in this repository. Copying twice gives byte-identical output.

import { mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? join(here, "out"));
const target = join(outDir, "entry.png");

const info = statSync(source);
if (!info.isFile()) {
  throw new Error(`entry.png missing next to main.ts (looked at ${source})`);
}

mkdirSync(outDir, { recursive: true });
writeFileSync(target, readFileSync(source));
console.log(`wrote ${target} (${info.size} bytes)`);
