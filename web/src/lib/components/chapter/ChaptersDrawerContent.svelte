<script lang="ts">
	import type { ChapterItem, SortDirection } from '#lib/types/novel';
	import SearchBar from '#lib/components/SearchBar.svelte';
	import SortButton from '#lib/components/SortButton.svelte';
	import ChapterList from '#lib/components/ChapterList.svelte';
	import Pagination from '#lib/components/Pagination.svelte';

	let {
		chapters = [],
		lastReadSlug = null
	}: {
		chapters: ChapterItem[];
		lastReadSlug?: string | null;
	} = $props();

	let searchQuery = $state('');
	let sortOrder = $state<SortDirection>('asc');
	let currentPage = $state(1);
	const ITEMS_PER_PAGE = 20;

	$effect(() => {
		if (searchQuery !== undefined) {
			currentPage = 1;
		}
	});

	let filteredChapters = $derived.by(() => {
		let list = [...chapters];
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

	let totalPages = $derived(Math.max(1, Math.ceil(filteredChapters.length / ITEMS_PER_PAGE)));

	let paginatedChapters = $derived.by(() => {
		const start = (currentPage - 1) * ITEMS_PER_PAGE;
		return filteredChapters.slice(start, start + ITEMS_PER_PAGE);
	});
</script>

<div class="space-y-4">
	<div class="flex items-center gap-2">
		<SearchBar bind:value={searchQuery} />
		<SortButton bind:sortOrder onSortChange={() => (currentPage = 1)} />
	</div>

	{#if paginatedChapters.length > 0}
		<ChapterList chapters={paginatedChapters} {lastReadSlug} />
		<Pagination {currentPage} {totalPages} onPageChange={(p) => (currentPage = p)} />
	{:else}
		<div class="rounded-xl border border-border-main bg-surface p-6 text-center shadow-sm sm:p-8">
			<p class="text-xs text-text-muted sm:text-sm">
				No chapters found matching &ldquo;<span class="font-semibold text-text-primary"
					>{searchQuery}</span
				>&rdquo;
			</p>
		</div>
	{/if}
</div>
