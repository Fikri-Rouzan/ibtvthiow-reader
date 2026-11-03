<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { cubicOut } from 'svelte/easing';
	import { fade } from 'svelte/transition';
	import type { PageData } from './$types';
	import { getReaderSettings, setLastReadChapter, setReaderSettings } from '#lib/utils/storage';
	import type { DrawerType, ReaderSettings } from '#lib/types/reader';
	import MarkdownRenderer from '#lib/components/MarkdownRenderer.svelte';
	import FloatingToolbar from '#lib/components/chapter/FloatingToolbar.svelte';
	import Drawer from '#lib/components/chapter/Drawer.svelte';
	import ChaptersDrawerContent from '#lib/components/chapter/ChaptersDrawerContent.svelte';
	import SettingsDrawerContent from '#lib/components/chapter/SettingsDrawerContent.svelte';
	import Navigation from '#lib/components/chapter/Navigation.svelte';
	import KeyboardShortcuts from '#lib/components/chapter/KeyboardShortcuts.svelte';
	import GiscusComments from '#lib/components/chapter/GiscusComments.svelte';

	let { data }: { data: PageData } = $props();

	let settings = $state<ReaderSettings>(getReaderSettings());
	let activeDrawer = $state<DrawerType>(null);

	// Synchronize settings state directly with document CSS custom variables and localStorage
	$effect(() => {
		if (settings) {
			setReaderSettings(settings);
			if (typeof document !== 'undefined') {
				const docEl = document.documentElement;
				docEl.setAttribute('data-theme', settings.theme);
				docEl.style.setProperty('--reader-font-size', `${settings.fontSize}px`);
				docEl.style.setProperty('--reader-font-family', settings.fontFamily);
				docEl.style.setProperty('--reader-line-height', String(settings.lineHeight));
				docEl.style.setProperty('--reader-font-weight', String(settings.fontWeight));
				docEl.style.setProperty('--reader-text-align', settings.textAlign);
			}
		}
	});

	onMount(() => {
		if (data.chapter?.meta?.slug) {
			setLastReadChapter(data.chapter.meta.slug);
		}
	});

	// Cleanup theme attribute when navigating away from chapter view
	onDestroy(() => {
		if (typeof document !== 'undefined') {
			document.documentElement.removeAttribute('data-theme');
		}
	});
</script>

<svelte:head>
	<title>{data.chapter.meta.title} - {data.metadata.title}</title>
</svelte:head>

<div
	data-theme={settings.theme}
	class="flex min-h-screen flex-col bg-bg-main text-text-primary transition-colors duration-200"
>
	{#key data.chapter.meta.slug}
		<main
			in:fade={{ duration: 250, easing: cubicOut }}
			class="mx-auto w-full max-w-4xl grow space-y-8 px-4 py-6 sm:px-6 sm:py-10"
		>
			<!-- Article view -->
			<article class="space-y-6">
				{#key settings.fontFamily + settings.textAlign}
					<div in:fade={{ duration: 180, easing: cubicOut }} class="space-y-16 sm:space-y-20">
						<div class="flex flex-col items-center gap-5 pt-3 text-center sm:gap-6 sm:pt-5">
							<h1
								class="text-2xl leading-tight font-bold text-accent sm:text-3xl md:text-4xl lg:text-5xl"
							>
								{data.chapter.meta.title}
							</h1>
							<div class="h-1 w-28 rounded-full bg-accent sm:w-36 md:w-40"></div>
						</div>

						<!-- Chapter content -->
						<div
							class="chapter-content transition-[font-size, line-height, font-weight] mb-10 duration-300 ease-out sm:mb-14"
						>
							<MarkdownRenderer tokens={data.chapter.tokens} />
						</div>
					</div>
				{/key}
			</article>

			<!-- Bottom navigation -->
			<Navigation
				prevSlug={data.prevSlug}
				nextSlug={data.nextSlug}
				chapterIndex={data.chapter.meta.index}
			/>

			<!-- Keyboard shortcuts guide -->
			<KeyboardShortcuts />

			<!-- Comments section -->
			<GiscusComments term={data.chapter.meta.title} theme={settings.theme} />
		</main>
	{/key}

	<FloatingToolbar
		prevSlug={data.prevSlug}
		nextSlug={data.nextSlug}
		onToggleDrawer={(drawer) => (activeDrawer = drawer)}
	/>

	<Drawer
		isOpen={activeDrawer === 'chapters'}
		title="Chapters List"
		onClose={() => (activeDrawer = null)}
	>
		<ChaptersDrawerContent
			chapters={data.metadata.chapters}
			lastReadSlug={data.chapter.meta.slug}
		/>
	</Drawer>

	<Drawer
		isOpen={activeDrawer === 'settings'}
		title="Reader Settings"
		onClose={() => (activeDrawer = null)}
	>
		<SettingsDrawerContent bind:settings />
	</Drawer>
</div>
