<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve, asset } from '$app/paths';
	import type { PageData } from './$types';
	import { ArrowLeft, BookOpen, Play } from '@lucide/svelte';
	import { getLastReadChapter } from '#lib/utils/storage';
	import type { SortDirection } from '#lib/types/novel';
	import SearchBar from '#lib/components/SearchBar.svelte';
	import SortButton from '#lib/components/SortButton.svelte';
	import ChapterList from '#lib/components/ChapterList.svelte';
	import Pagination from '#lib/components/Pagination.svelte';

	// Server loader data containing novel metadata and chapter list
	let { data }: { data: PageData } = $props();

	// Reactive state for reading history, catalog filtering, and pagination
	let lastReadSlug = $state<string | null>(null);
	let searchQuery = $state('');
	let sortOrder = $state<SortDirection>('asc');
	let currentPage = $state(1);
	const ITEMS_PER_PAGE = 20;

	// Retrieve user's last read chapter slug from browser localStorage on mount
	onMount(() => {
		lastReadSlug = getLastReadChapter();
	});

	// Automatically reset pagination to page 1 whenever search query updates
	$effect(() => {
		if (searchQuery !== undefined) {
			currentPage = 1;
		}
	});

	// Derived state: Filter chapters by title/slug/index and apply sort order
	let filteredChapters = $derived.by(() => {
		let list = [...data.metadata.chapters];

		if (searchQuery.trim()) {
			const q = searchQuery.toLowerCase().trim();
			list = list.filter(
				(ch) =>
					ch.title.toLowerCase().includes(q) || ch.index.toString() === q || ch.slug.includes(q)
			);
		}

		if (sortOrder === 'desc') {
			list.reverse();
		}

		return list;
	});

	// Calculate total pages dynamically based on filtered chapters count
	let totalPages = $derived(Math.max(1, Math.ceil(filteredChapters.length / ITEMS_PER_PAGE)));

	// Slice filtered chapters list for current active page
	let paginatedChapters = $derived.by(() => {
		const start = (currentPage - 1) * ITEMS_PER_PAGE;
		return filteredChapters.slice(start, start + ITEMS_PER_PAGE);
	});

	// Compute CTA destination slug and label dynamically based on reading history
	let ctaSlug = $derived(lastReadSlug || '000');
	let ctaLabel = $derived(lastReadSlug ? 'Continue Reading' : 'Start Reading');
</script>

<svelte:head>
	<title>{data.metadata.title}</title>
</svelte:head>

<div class="relative flex grow bg-[url('/assets/background.jpg')] bg-cover bg-fixed bg-center">
	<!-- Floating back icon -->
	<a
		href={resolve('/')}
		aria-label="Go back"
		title="Go Back"
		class="fixed top-6 left-4 z-50 inline-flex cursor-pointer items-center justify-center rounded-full border border-border-main bg-surface/80 p-2.5 text-text-muted shadow-lg backdrop-blur-md transition-colors hover:border-accent hover:text-accent sm:top-8 sm:left-6"
	>
		<ArrowLeft class="h-5 w-5 sm:h-6 sm:w-6" />
	</a>

	<div class="flex grow flex-col bg-bg-main/80">
		<main
			class="mx-auto w-full max-w-5xl grow space-y-10 px-4 pt-10 pb-6 sm:px-6 sm:pt-14 sm:pb-10"
		>
			<header class="grid grid-cols-1 items-start gap-6 md:grid-cols-12">
				<!-- Left column: Cover image and CTA -->
				<div class="flex flex-col items-center gap-4 md:col-span-4 md:items-start lg:col-span-3">
					<figure class="w-56 sm:w-64 md:w-full">
						<img
							src={asset('assets/cover.jpg')}
							alt={data.metadata.title}
							class="aspect-3/4 w-full rounded-xl border border-border-main object-cover shadow-2xl"
						/>
					</figure>

					<a
						href={resolve('/ibtvthiow/chapter/[slug]', { slug: ctaSlug })}
						class="flex w-56 items-center justify-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-xs font-bold text-bg-main shadow-md transition-colors hover:bg-accent-hover sm:w-64 sm:py-3 sm:text-sm md:w-full"
					>
						{#if lastReadSlug}
							<Play class="h-4 w-4 shrink-0 fill-current sm:h-5 sm:w-5" />
						{:else}
							<BookOpen class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
						{/if}
						<span>{ctaLabel}</span>
					</a>
				</div>

				<!-- Right column: Metadata overview -->
				<div class="space-y-3 pt-1 text-left md:col-span-8 md:pt-2 lg:col-span-9">
					<h1 class="text-2xl leading-tight font-bold text-accent sm:text-3xl md:text-4xl">
						{data.metadata.title}
					</h1>

					<div class="space-y-1 text-xs text-text-secondary sm:text-sm md:text-base">
						<p><span class="text-text-muted">Author:</span> {data.metadata.author}</p>
						<p>
							<span class="text-text-muted">Total Chapters:</span>
							{data.metadata.total_chapters}
						</p>
						<p><span class="text-text-muted">Status:</span> {data.metadata.status}</p>
					</div>

					<div
						class="space-y-2 pt-2 text-xs leading-relaxed text-text-secondary sm:text-sm md:text-base"
					>
						{#each data.metadata.synopsis as paragraph, idx (`synopsis-${idx}`)}
							<p>{paragraph}</p>
						{/each}
					</div>
				</div>
			</header>

			<!-- Catalog controls & Chapter list -->
			<section class="space-y-4 pt-2" aria-label="Chapter catalog and controls">
				<div class="flex items-center gap-2">
					<SearchBar bind:value={searchQuery} />
					<SortButton bind:sortOrder onSortChange={() => (currentPage = 1)} />
				</div>

				{#if paginatedChapters.length > 0}
					<ChapterList chapters={paginatedChapters} {lastReadSlug} />
					<Pagination {currentPage} {totalPages} onPageChange={(p) => (currentPage = p)} />
				{:else}
					<div class="rounded-xl border border-border-main bg-surface p-8 text-center shadow-sm">
						<p class="text-xs text-text-muted sm:text-sm">
							No chapters found matching &ldquo;<span class="font-semibold text-text-primary"
								>{searchQuery}</span
							>&rdquo;
						</p>
					</div>
				{/if}
			</section>
		</main>
	</div>
</div>
