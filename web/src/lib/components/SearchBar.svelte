<script lang="ts">
	import { Search, X } from '@lucide/svelte';

	let { value = $bindable('') }: { value: string } = $props();
</script>

<div class="relative w-full grow">
	<Search class="absolute top-1/2 left-3.5 h-4 w-4 -translate-y-1/2 text-text-muted" />
	<input
		id="chapter-search"
		name="chapter-search"
		type="text"
		bind:value
		placeholder="Search chapter..."
		aria-label="Search chapter list"
		class="w-full rounded-lg border border-border-main bg-surface py-2 pr-10 pl-10 text-xs text-text-primary placeholder-text-muted transition-colors focus:border-accent focus:ring-0 focus:outline-none sm:py-2.5 sm:text-sm"
	/>
	{#if value}
		<button
			type="button"
			onclick={() => (value = '')}
			title="Clear Search Query"
			aria-label="Clear search query"
			class="absolute top-1/2 right-3 -translate-y-1/2 cursor-pointer text-text-muted transition-colors hover:text-text-primary"
		>
			<X class="h-4 w-4" />
		</button>
	{/if}
</div>
