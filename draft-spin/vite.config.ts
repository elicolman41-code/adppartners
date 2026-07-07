import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { viteSingleFile } from 'vite-plugin-singlefile';

// Single-file output so the game can be opened directly on a phone,
// matching how other apps in this repo are delivered.
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: { outDir: 'dist' },
});
