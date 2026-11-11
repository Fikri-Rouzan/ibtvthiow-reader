import tailwindcss from '@tailwindcss/vite';
import adapter from '@sveltejs/adapter-cloudflare';
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig, normalizePath } from 'vite';
import { viteStaticCopy } from 'vite-plugin-static-copy';
import path from 'node:path';

// Resolve and normalize absolute path to root /images directory for cross-platform globbing
const imagesPath = normalizePath(path.resolve(import.meta.dirname, '../images'));

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit({
			compilerOptions: {
				// Force runes mode for the project, except for libraries. Can be removed in svelte 6.
				runes: ({ filename }) =>
					filename.split(/[/\\]/).includes('node_modules') ? undefined : true
			},
			adapter: adapter()
		}),
		// Copy images directory directly into the client build output root
		viteStaticCopy({
			targets: [
				{
					src: imagesPath,
					dest: ''
				}
			]
		})
	]
});
