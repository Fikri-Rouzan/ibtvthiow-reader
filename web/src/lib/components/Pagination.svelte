<script lang="ts">
	import {
		getPaginationItems,
		NAV_BUTTONS_LEFT,
		NAV_BUTTONS_RIGHT,
		NAV_BTN_CLASS
	} from '#lib/utils/pagination';

	let {
		currentPage,
		totalPages,
		onPageChange
	}: {
		currentPage: number;
		totalPages: number;
		onPageChange: (page: number) => void;
	} = $props();

	let paginationItems = $derived(getPaginationItems(currentPage, totalPages));
</script>

{#if totalPages > 1}
	<div
		class="mt-3 flex items-center justify-center gap-1 border-t border-border-main pt-3 sm:mt-4 sm:gap-1.5 sm:pt-4"
	>
		<!-- Left navigation controls (First & Prev) -->
		{#each NAV_BUTTONS_LEFT as btn (btn.id)}
			{@const Icon = btn.icon}
			<button
				type="button"
				disabled={btn.disabled(currentPage, totalPages)}
				onclick={() => onPageChange(btn.targetPage(currentPage, totalPages))}
				class={NAV_BTN_CLASS}
				title={btn.title}
			>
				<Icon class="h-3.5 w-3.5 shrink-0 sm:h-4 sm:w-4" />
			</button>
		{/each}

		<!-- Page number buttons & Ellipses -->
		{#each paginationItems as item, idx (`${item}-${idx}`)}
			{#if typeof item === 'number'}
				<button
					type="button"
					onclick={() => onPageChange(item)}
					class="inline-flex h-7 min-w-7 cursor-pointer items-center justify-center rounded-md px-2 text-xs font-semibold transition-colors sm:h-8 sm:min-w-8 sm:px-3 sm:text-sm {item ===
					currentPage
						? 'border border-accent bg-accent font-bold text-bg-main'
						: 'border border-border-main bg-surface text-text-muted hover:bg-surface-hover'}"
				>
					{item}
				</button>
			{:else}
				<span
					class="cursor-default px-0.5 text-xs font-semibold text-text-muted select-none sm:px-1 sm:text-sm"
				>
					{item}
				</span>
			{/if}
		{/each}

		<!-- Right Navigation Controls (Next & Last) -->
		{#each NAV_BUTTONS_RIGHT as btn (btn.id)}
			{@const Icon = btn.icon}
			<button
				type="button"
				disabled={btn.disabled(currentPage, totalPages)}
				onclick={() => onPageChange(btn.targetPage(currentPage, totalPages))}
				class={NAV_BTN_CLASS}
				title={btn.title}
			>
				<Icon class="h-3.5 w-3.5 shrink-0 sm:h-4 sm:w-4" />
			</button>
		{/each}
	</div>
{/if}
