<script lang="ts">
	import { Keyboard } from '@lucide/svelte';

	const SHORTCUTS = [
		{ key: 'H', label: 'Home' },
		{ key: 'T', label: 'Chapters List' },
		{ key: 'C', label: 'Comments' },
		{ key: 'P', label: 'Auto Scroll' },
		{ key: 'F', label: 'Fullscreen' },
		{ key: 'A / ←', label: 'Previous' },
		{ key: 'D / →', label: 'Next' },
		{ key: 'S', label: 'Settings' },
		{ key: 'M', label: 'Toolbar' },
		{ key: 'Esc', label: 'Close Drawer' }
	];
</script>

<section
	class="my-10 rounded-xl border border-border-main bg-surface p-5 shadow-sm sm:my-12 sm:p-6"
	aria-label="Keyboard Shortcuts Guide"
>
	<div
		class="mb-4 flex items-center justify-center gap-2 border-b border-border-main pb-3 text-center sm:mb-5"
	>
		<Keyboard class="h-4 w-4 text-accent sm:h-5 sm:w-5" />
		<h2 class="text-xs font-bold tracking-wider text-text-primary uppercase sm:text-sm">
			Keyboard Shortcuts
		</h2>
	</div>

	<div class="grid grid-cols-2 gap-x-4 gap-y-3 sm:grid-cols-3 sm:gap-x-6 sm:gap-y-3.5">
		{#each SHORTCUTS as item (item.key)}
			<div class="flex items-center gap-2">
				<kbd
					class="rounded border border-border-main bg-bg-main px-2 py-0.5 font-mono text-[10px] font-bold text-accent sm:text-xs"
				>
					{item.key}
				</kbd>
				<span class="truncate text-[11px] font-medium text-text-secondary sm:text-xs">
					{item.label}
				</span>
			</div>
		{/each}
	</div>
</section>
