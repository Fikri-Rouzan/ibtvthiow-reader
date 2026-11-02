<script lang="ts">
	import './layout.css';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();

	// Clear reader data-theme immediately if the route is not a valid chapter or returns an error status (e.g. 404)
	$effect(() => {
		const isChapterPage = page.url.pathname.includes('/ibtvthiow/chapter/');
		const isErrorPage = page.status >= 400;

		if (typeof document !== 'undefined') {
			if (!isChapterPage || isErrorPage) {
				document.documentElement.removeAttribute('data-theme');
			}
		}
	});

	// Reveal page container smoothly after DOM hydration, theme sync, and scroll restoration complete
	onMount(() => {
		requestAnimationFrame(() => {
			document.documentElement.classList.remove('page-loading');
			requestAnimationFrame(() => {
				document.documentElement.classList.remove('no-transitions');
			});
		});
	});
</script>

<div
	data-page-container
	class="flex min-h-screen flex-col bg-bg-main font-sans text-text-primary antialiased"
>
	{@render children()}
</div>
