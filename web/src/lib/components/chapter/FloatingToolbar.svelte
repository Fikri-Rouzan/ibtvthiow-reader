<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import type { DrawerType } from '#lib/types/reader';
	import {
		ChevronLeft,
		ChevronRight,
		House,
		List,
		Maximize,
		Minimize,
		MessageSquare,
		Pause,
		Play,
		Settings
	} from '@lucide/svelte';

	let {
		prevSlug = null,
		nextSlug = null,
		onToggleDrawer
	}: {
		prevSlug?: string | null;
		nextSlug?: string | null;
		onToggleDrawer: (drawer: DrawerType) => void;
	} = $props();

	let isMenuVisible = $state(true);
	let isAutoScrolling = $state(false);
	let isFullscreen = $state(false);

	// Auto-scroll state variables tracking absolute sub-pixel position
	let animationFrameId: number | null = null;
	const SCROLL_SPEED = 0.2;
	let scrollAccumulator = 0;
	let lastScrollY = 0;

	const TOOLBAR_BTN_CLASS =
		'inline-flex items-center justify-center rounded-xl p-2 transition-colors hover:bg-surface-hover hover:text-accent sm:p-2.5';
	const TOOLBAR_ICON_CLASS = 'h-4 w-4 sm:h-5 sm:w-5';

	/**
	 * Checks if the keyboard event originated from an interactive text input element.
	 */
	function isUserTyping(e: KeyboardEvent): boolean {
		const target = e.target as HTMLElement | null;
		if (!target) return false;
		const tagName = target.tagName.toUpperCase();
		return (
			tagName === 'INPUT' ||
			tagName === 'TEXTAREA' ||
			tagName === 'SELECT' ||
			target.isContentEditable
		);
	}

	function scrollToComments() {
		const commentsEl = document.getElementById('comments-section');
		if (commentsEl) {
			commentsEl.scrollIntoView({ behavior: 'smooth' });
		}
	}

	function handleKeydown(e: KeyboardEvent) {
		if (isUserTyping(e)) return;

		const key = e.key.toLowerCase();

		switch (key) {
			case 'm':
				e.preventDefault();
				isMenuVisible = !isMenuVisible;
				break;
			case 'h':
				e.preventDefault();
				goto(resolve('/ibtvthiow'));
				break;
			case 't':
				e.preventDefault();
				onToggleDrawer('chapters');
				break;
			case 'c':
				e.preventDefault();
				scrollToComments();
				break;
			case 'p':
				e.preventDefault();
				toggleAutoScroll();
				break;
			case 'f':
				e.preventDefault();
				toggleFullscreen();
				break;
			case 'a':
			case 'arrowleft':
				if (prevSlug) {
					e.preventDefault();
					goto(resolve('/ibtvthiow/chapter/[slug]', { slug: prevSlug }));
				}
				break;
			case 'd':
			case 'arrowright':
				if (nextSlug) {
					e.preventDefault();
					goto(resolve('/ibtvthiow/chapter/[slug]', { slug: nextSlug }));
				}
				break;
			case 's':
				e.preventDefault();
				onToggleDrawer('settings');
				break;
		}
	}

	function toggleAutoScroll() {
		isAutoScrolling = !isAutoScrolling;
		if (isAutoScrolling) {
			startAutoScroll();
		} else {
			stopAutoScroll();
		}
	}

	/**
	 * Sub-pixel absolute auto-scroll step function.
	 */
	function startAutoScroll() {
		scrollAccumulator = window.scrollY;

		const scrollStep = () => {
			if (!isAutoScrolling) return;

			const maxScroll = document.documentElement.scrollHeight - window.innerHeight;
			if (window.scrollY >= maxScroll - 2) {
				stopAutoScroll();
				return;
			}

			scrollAccumulator += SCROLL_SPEED;
			window.scrollTo(0, scrollAccumulator);

			animationFrameId = requestAnimationFrame(scrollStep);
		};

		animationFrameId = requestAnimationFrame(scrollStep);
	}

	function stopAutoScroll() {
		isAutoScrolling = false;
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}
	}

	function toggleFullscreen() {
		if (!document.fullscreenElement) {
			document.documentElement
				.requestFullscreen()
				.then(() => (isFullscreen = true))
				.catch(() => {});
		} else {
			document
				.exitFullscreen()
				.then(() => (isFullscreen = false))
				.catch(() => {});
		}
	}

	onMount(() => {
		lastScrollY = window.scrollY;

		// Hide toolbar only when user performs significant manual scroll
		const handleScroll = () => {
			if (isAutoScrolling) return;
			const currentScrollY = window.scrollY;
			if (Math.abs(currentScrollY - lastScrollY) > 15) {
				if (isMenuVisible) {
					isMenuVisible = false;
				}
				lastScrollY = currentScrollY;
			}
		};

		// Universal single tap / single click handler for mobile & desktop
		const handleClick = (e: MouseEvent) => {
			const target = e.target as HTMLElement | null;
			if (!target) return;

			// Ignore click if it occurs inside the floating toolbar container
			const menuElement = document.getElementById('floating-menu');
			if (menuElement && menuElement.contains(target)) return;

			// Ignore click if it originates from an interactive element
			if (target.closest('a, button, input, textarea, select, details, [role="button"]')) {
				return;
			}

			// Ignore click if the user is actively selecting text
			const selection = window.getSelection();
			if (selection && selection.toString().trim().length > 0) return;

			isMenuVisible = !isMenuVisible;
		};

		const handleFullscreenChange = () => {
			isFullscreen = !!document.fullscreenElement;
		};

		window.addEventListener('scroll', handleScroll, { passive: true });
		window.addEventListener('click', handleClick);
		document.addEventListener('fullscreenchange', handleFullscreenChange);

		return () => {
			stopAutoScroll();
			window.removeEventListener('scroll', handleScroll);
			window.removeEventListener('click', handleClick);
			document.removeEventListener('fullscreenchange', handleFullscreenChange);
		};
	});
</script>

<!-- Window event listener for shortcuts -->
<svelte:window onkeydown={handleKeydown} />

<div
	id="floating-menu"
	class="fixed top-1/2 right-2.5 z-40 flex -translate-y-1/2 flex-col gap-1.5 rounded-2xl border border-border-main bg-surface/90 p-1.5 shadow-2xl backdrop-blur-md transition-opacity duration-300 sm:right-4 sm:gap-2 sm:p-2 {isMenuVisible
		? 'opacity-100'
		: 'pointer-events-none opacity-0'}"
>
	<!-- Home -->
	<a
		href={resolve('/ibtvthiow')}
		aria-label="Home"
		title="Home (H)"
		class="{TOOLBAR_BTN_CLASS} text-text-muted"
	>
		<House class={TOOLBAR_ICON_CLASS} />
	</a>

	<!-- Chapters list -->
	<button
		type="button"
		onclick={() => onToggleDrawer('chapters')}
		aria-label="Chapters List"
		title="Chapters List (T)"
		class="{TOOLBAR_BTN_CLASS} cursor-pointer text-text-muted"
	>
		<List class={TOOLBAR_ICON_CLASS} />
	</button>

	<!-- Jump to comments -->
	<button
		type="button"
		onclick={scrollToComments}
		aria-label="Jump to Comments"
		title="Comments (C)"
		class="{TOOLBAR_BTN_CLASS} cursor-pointer text-text-muted"
	>
		<MessageSquare class={TOOLBAR_ICON_CLASS} />
	</button>

	<!-- Auto scroll -->
	<button
		type="button"
		onclick={toggleAutoScroll}
		aria-label={isAutoScrolling ? 'Pause Auto Scroll' : 'Play Auto Scroll'}
		title={isAutoScrolling ? 'Pause Auto Scroll (P)' : 'Play Auto Scroll (P)'}
		class="{TOOLBAR_BTN_CLASS} cursor-pointer {isAutoScrolling ? 'text-accent' : 'text-text-muted'}"
	>
		{#if isAutoScrolling}
			<Pause class={TOOLBAR_ICON_CLASS} />
		{:else}
			<Play class={TOOLBAR_ICON_CLASS} />
		{/if}
	</button>

	<!-- Fullscreen toggle -->
	<button
		type="button"
		onclick={toggleFullscreen}
		aria-label={isFullscreen ? 'Exit Fullscreen' : 'Enter Fullscreen'}
		title={isFullscreen ? 'Exit Fullscreen (F)' : 'Enter Fullscreen (F)'}
		class="{TOOLBAR_BTN_CLASS} cursor-pointer {isFullscreen ? 'text-accent' : 'text-text-muted'}"
	>
		{#if isFullscreen}
			<Minimize class={TOOLBAR_ICON_CLASS} />
		{:else}
			<Maximize class={TOOLBAR_ICON_CLASS} />
		{/if}
	</button>

	<!-- Previous chapter -->
	{#if prevSlug}
		<a
			href={resolve('/ibtvthiow/chapter/[slug]', { slug: prevSlug })}
			aria-label="Previous Chapter"
			title="Previous (A)"
			class="{TOOLBAR_BTN_CLASS} text-text-muted"
		>
			<ChevronLeft class={TOOLBAR_ICON_CLASS} />
		</a>
	{:else}
		<button
			type="button"
			disabled
			aria-label="No Previous Chapter"
			title="First Chapter"
			class="{TOOLBAR_BTN_CLASS} cursor-not-allowed text-text-muted/30"
		>
			<ChevronLeft class={TOOLBAR_ICON_CLASS} />
		</button>
	{/if}

	<!-- Next chapter -->
	{#if nextSlug}
		<a
			href={resolve('/ibtvthiow/chapter/[slug]', { slug: nextSlug })}
			aria-label="Next Chapter"
			title="Next (D)"
			class="{TOOLBAR_BTN_CLASS} text-text-muted"
		>
			<ChevronRight class={TOOLBAR_ICON_CLASS} />
		</a>
	{:else}
		<button
			type="button"
			disabled
			aria-label="No Next Chapter"
			title="Final Chapter"
			class="{TOOLBAR_BTN_CLASS} cursor-not-allowed text-text-muted/30"
		>
			<ChevronRight class={TOOLBAR_ICON_CLASS} />
		</button>
	{/if}

	<!-- Reader settings -->
	<button
		type="button"
		onclick={() => onToggleDrawer('settings')}
		aria-label="Reader Settings"
		title="Settings (S)"
		class="{TOOLBAR_BTN_CLASS} cursor-pointer text-text-muted"
	>
		<Settings class={TOOLBAR_ICON_CLASS} />
	</button>
</div>
