<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import type { PageData } from './$types';
	import { ArrowLeft, ArrowRight, Home } from '@lucide/svelte';
	import { setLastReadChapter } from '#lib/utils/storage';
	import MarkdownRenderer from '#lib/components/MarkdownRenderer.svelte';

	let { data }: { data: PageData } = $props();

	onMount(() => {
		if (data.chapter?.meta?.slug) {
			setLastReadChapter(data.chapter.meta.slug);
		}
	});
</script>

<svelte:head>
	<title>{data.chapter.meta.title} - {data.metadata.title}</title>
</svelte:head>

<main class="mx-auto w-full max-w-4xl grow space-y-8 px-4 py-6 sm:px-6 sm:py-10">
	<!-- Article view -->
	<article class="space-y-6">
		<h1
			class="border-b border-border-main pb-4 text-center text-xl leading-tight font-bold text-accent sm:text-2xl md:text-3xl lg:text-4xl"
		>
			{data.chapter.meta.title}
		</h1>

		<!-- Render markdown via token components -->
		<MarkdownRenderer tokens={data.chapter.tokens} />
	</article>

	<!-- Bottom chapter navigation -->
	<nav
		class="flex items-center justify-between border-t border-border-main pt-6"
		aria-label="Chapter navigation"
	>
		{#if data.prevSlug !== null}
			<a
				href={resolve('/ibtvthiow/chapter/[slug]', { slug: data.prevSlug })}
				class="inline-flex items-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-accent hover:text-bg-main sm:px-5 sm:py-3 sm:text-sm"
			>
				<ArrowLeft class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
				<span>Previous</span>
			</a>
		{:else}
			<a
				href={resolve('/ibtvthiow')}
				class="inline-flex items-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-accent hover:text-bg-main sm:px-5 sm:py-3 sm:text-sm"
			>
				<Home class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
				<span>Home</span>
			</a>
		{/if}

		{#if data.nextSlug !== null}
			<a
				href={resolve('/ibtvthiow/chapter/[slug]', { slug: data.nextSlug })}
				class="inline-flex items-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-accent hover:text-bg-main sm:px-5 sm:py-3 sm:text-sm"
			>
				<span>Next</span>
				<ArrowRight class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
			</a>
		{:else}
			<a
				href={resolve('/ibtvthiow')}
				class="inline-flex items-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-accent hover:text-bg-main sm:px-5 sm:py-3 sm:text-sm"
			>
				<span>Home</span>
				<Home class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
			</a>
		{/if}
	</nav>
</main>
