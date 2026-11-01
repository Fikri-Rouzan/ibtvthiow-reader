<script lang="ts">
	import { ArrowDown, ArrowUp } from '@lucide/svelte';
	import type { SortDirection } from '#lib/types/novel';

	let {
		sortOrder = $bindable('asc'),
		onSortChange
	}: {
		sortOrder: SortDirection;
		onSortChange?: () => void;
	} = $props();

	function toggleSort() {
		sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
		if (onSortChange) {
			onSortChange();
		}
	}
</script>

<button
	type="button"
	onclick={toggleSort}
	aria-label="Toggle chapter sort order"
	title={sortOrder === 'asc' ? 'Ascending Order' : 'Descending Order'}
	class="inline-flex h-9 shrink-0 cursor-pointer items-center gap-1.5 rounded-lg border border-border-main bg-surface px-3 text-xs font-semibold text-text-secondary transition-colors hover:bg-surface-hover hover:text-text-primary sm:h-10 sm:px-4 sm:text-sm"
>
	<span class="hidden sm:inline">{sortOrder === 'asc' ? 'Ascending' : 'Descending'}</span>
	<span class="uppercase sm:hidden">{sortOrder}</span>
	{#if sortOrder === 'asc'}
		<ArrowUp class="h-3.5 w-3.5 text-accent sm:h-4 sm:w-4" />
	{:else}
		<ArrowDown class="h-3.5 w-3.5 text-accent sm:h-4 sm:w-4" />
	{/if}
</button>
