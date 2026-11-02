<script lang="ts">
	import type { Snippet } from 'svelte';
	import { cubicOut } from 'svelte/easing';
	import { fade, fly } from 'svelte/transition';
	import { X } from '@lucide/svelte';

	let {
		isOpen = false,
		title = '',
		onClose,
		children
	}: {
		isOpen: boolean;
		title: string;
		onClose: () => void;
		children: Snippet;
	} = $props();

	// Lock document body scroll while drawer is open
	$effect(() => {
		if (typeof document === 'undefined') return;
		if (isOpen) {
			document.body.style.overflow = 'hidden';
		} else {
			document.body.style.overflow = '';
		}
		return () => {
			document.body.style.overflow = '';
		};
	});

	// Global window keydown listener
	function handleKeydown(e: KeyboardEvent) {
		if (isOpen && e.key === 'Escape') {
			onClose();
		}
	}
</script>

<!-- Global event listener for keyboard shortcuts -->
<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
	<!-- Backdrop overlay -->
	<button
		type="button"
		tabindex="-1"
		aria-label="Close drawer backdrop"
		onclick={onClose}
		transition:fade={{ duration: 250, easing: cubicOut }}
		class="fixed inset-0 z-50 cursor-default border-0 bg-bg-main/60 outline-none"
	></button>

	<!-- Drawer panel -->
	<aside
		transition:fly={{ x: 340, duration: 300, easing: cubicOut }}
		class="fixed top-0 right-0 z-50 h-full w-full max-w-[75vw] overflow-y-auto border-l border-border-main bg-bg-main p-4 shadow-2xl transition-colors duration-200 sm:max-w-lg sm:p-6"
		aria-label={title}
	>
		<!-- Drawer header -->
		<div
			class="mb-4 flex items-center justify-between border-b border-border-main pb-3 sm:mb-6 sm:pb-4"
		>
			<h2 class="text-base font-bold text-text-primary sm:text-lg">{title}</h2>
			<button
				type="button"
				onclick={onClose}
				aria-label="Close drawer"
				title="Close (Esc)"
				class="cursor-pointer rounded-lg p-1.5 text-text-muted transition-colors hover:bg-surface-hover hover:text-text-primary"
			>
				<X class="h-5 w-5" />
			</button>
		</div>

		<!-- Drawer inner body -->
		{@render children()}
	</aside>
{/if}
