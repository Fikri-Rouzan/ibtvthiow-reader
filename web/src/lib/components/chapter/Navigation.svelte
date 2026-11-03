<script lang="ts">
	import { resolve } from '$app/paths';
	import { ArrowLeft, ArrowRight, House } from '@lucide/svelte';

	let {
		prevSlug = null,
		nextSlug = null,
		chapterIndex
	}: {
		prevSlug?: string | null;
		nextSlug?: string | null;
		chapterIndex?: number | string;
	} = $props();

	const NAV_BTN_CLASS =
		'inline-flex items-center gap-2 rounded-xl border border-accent bg-surface px-3.5 py-2.5 text-xs font-semibold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-accent hover:text-bg-main sm:px-5 sm:py-3 sm:text-sm';
	const NAV_ICON_CLASS = 'h-4 w-4 shrink-0 sm:h-5 sm:w-5';
</script>

<nav
	class="flex items-center justify-between border-t border-border-main pt-6"
	aria-label="Chapter navigation"
>
	<!-- Previous / Home button -->
	{#if prevSlug !== null}
		<a href={resolve('/ibtvthiow/chapter/[slug]', { slug: prevSlug })} class={NAV_BTN_CLASS}>
			<ArrowLeft class={NAV_ICON_CLASS} />
			<span>Previous</span>
		</a>
	{:else}
		<a href={resolve('/ibtvthiow')} class={NAV_BTN_CLASS}>
			<House class={NAV_ICON_CLASS} />
			<span>Home</span>
		</a>
	{/if}

	<!-- Chapter indicator -->
	{#if chapterIndex !== undefined && chapterIndex !== null}
		<span class="font-mono text-xs font-bold tracking-wider text-accent sm:text-sm">
			CH. {chapterIndex}
		</span>
	{/if}

	<!-- Next / Home button -->
	{#if nextSlug !== null}
		<a href={resolve('/ibtvthiow/chapter/[slug]', { slug: nextSlug })} class={NAV_BTN_CLASS}>
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
