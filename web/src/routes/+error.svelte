<script lang="ts">
	import { onMount } from 'svelte';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { ArrowLeft, Globe } from '@lucide/svelte';

	function goBack() {
		if (typeof window !== 'undefined') {
			window.history.back();
		}
	}

	// Ensure reader theme attribute is stripped immediately on error page mount
	onMount(() => {
		if (typeof document !== 'undefined') {
			document.documentElement.removeAttribute('data-theme');
		}
	});

	$effect(() => {
		if (typeof document !== 'undefined') {
			document.documentElement.removeAttribute('data-theme');
		}
	});
</script>

<svelte:head>
	<title>{page.status || 404} - Not Found</title>
</svelte:head>

<div
	class="relative flex grow bg-[url('/assets/background.jpg')] bg-cover bg-scroll bg-center md:bg-fixed"
>
	<div class="flex grow items-center justify-center bg-bg-main/80 px-4 text-center sm:px-6">
		<main class="flex max-w-xl flex-col items-center space-y-6">
			<h1 class="text-6xl font-extrabold tracking-tight text-accent sm:text-7xl md:text-8xl">
				{page.status || 404}
			</h1>

			<p
				class="text-sm leading-relaxed font-medium text-text-secondary italic sm:text-base md:text-lg"
			>
				&ldquo;A half-real, half-fake world, just like a dream.&rdquo;
			</p>

			<div class="flex flex-row items-center justify-center gap-2.5 pt-2 sm:gap-4">
				<button
					type="button"
					onclick={goBack}
					class="inline-flex cursor-pointer items-center justify-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-lg transition-colors hover:border-accent-hover hover:bg-surface-hover sm:px-6 sm:py-3.5 sm:text-base"
				>
					<ArrowLeft class="h-4 w-4 shrink-0 text-accent sm:h-5 sm:w-5" />
					<span>Back</span>
				</button>
				<a
					href={resolve('/')}
					class="inline-flex items-center justify-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-xs font-semibold text-bg-main shadow-lg transition-colors hover:bg-accent-hover sm:px-6 sm:py-3.5 sm:text-base"
				>
					<Globe class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
					<span>Return to the World</span>
				</a>
			</div>
		</main>
	</div>
</div>
