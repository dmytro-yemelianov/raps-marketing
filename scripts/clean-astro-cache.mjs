import { rmSync } from 'node:fs';
import { join } from 'node:path';

const cacheFile = join(process.cwd(), '.astro', 'data-store.json');

rmSync(cacheFile, { force: true });
