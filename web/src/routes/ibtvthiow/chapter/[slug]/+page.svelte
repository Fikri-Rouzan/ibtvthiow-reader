<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import { cubicOut } from 'svelte/easing';
	import { fade } from 'svelte/transition';
	import { resolve } from '$app/paths';
	import type { PageData } from './$types';
	import { getReaderSettings, setLastReadChapter, setReaderSettings } from '#lib/utils/storage';
	import type { DrawerType, ReaderSettings } from '#lib/types/reader';
	import MarkdownRenderer from '#lib/components/MarkdownRenderer.svelte';
	import FloatingToolbar from '#lib/components/chapter/FloatingToolbar.svelte';
	import Drawer from '#lib/components/chapter/Drawer.svelte';
	import ChaptersDrawerContent from '#lib/components/chapter/ChaptersDrawerContent.svelte';
	import SettingsDrawerContent from '#lib/components/chapter/SettingsDrawerContent.svelte';
	import { ArrowLeft, ArrowRight, House } from '@lucide/svelte';

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

	const NAV_BTN_CLASS =
		'inline-flex items-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-accent hover:text-bg-main sm:px-5 sm:py-3 sm:text-sm';
	const NAV_ICON_CLASS = 'h-4 w-4 shrink-0 sm:h-5 sm:w-5';
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
				<h1
					class="border-b border-border-main pb-4 text-center text-2xl leading-tight font-bold text-accent sm:text-3xl md:text-4xl lg:text-5xl"
				>
					{data.chapter.meta.title}
				</h1>

				<!-- Chapter content -->
				<div
					class="chapter-content transition-[font-size, line-height, font-weight] duration-300 ease-out"
				>
					{#key settings.fontFamily + settings.textAlign}
						<div in:fade={{ duration: 180, easing: cubicOut }}>
							<MarkdownRenderer tokens={data.chapter.tokens} />
						</div>
					{/key}
				</div>
			</article>

			<!-- Bottom navigation -->
			<nav
				class="flex items-center justify-between border-t border-border-main pt-6"
				aria-label="Chapter navigation"
			>
				{#if data.prevSlug !== null}
					<a
						href={resolve('/ibtvthiow/chapter/[slug]', { slug: data.prevSlug })}
						class={NAV_BTN_CLASS}
					>
						<ArrowLeft class={NAV_ICON_CLASS} />
						<span>Previous</span>
					</a>
				{:else}
					<a href={resolve('/ibtvthiow')} class={NAV_BTN_CLASS}>
						<House class={NAV_ICON_CLASS} />
						<span>Home</span>
					</a>
				{/if}

				{#if data.nextSlug !== null}
					<a
						href={resolve('/ibtvthiow/chapter/[slug]', { slug: data.nextSlug })}
						class={NAV_BTN_CLASS}
					>
						<span>Next</span>
						<ArrowRight class={NAV_ICON_CLASS} />
					</a>
				{:else}
					<a href={resolve('/ibtvthiow')} class={NAV_BTN_CLASS}>
						<span>Home</span>
						<House class={NAV_ICON_CLASS} />
					</a>
				{/if}
			</nav>
		</main>
	{/key}

	<FloatingToolbar
		prevSlug={data.prevSlug}
		nextSlug={data.nextSlug}
		onToggleDrawer={(drawer) => (activeDrawer = drawer)}
	/>

	<Drawer
		isOpen={activeDrawer === 'chapters'}
		title="Table of Contents"
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
