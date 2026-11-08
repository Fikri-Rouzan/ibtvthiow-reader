<script lang="ts">
	import { resolve } from '$app/paths';
	import type { PageData } from './$types';
	import { ArrowLeft, Download } from '@lucide/svelte';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>Download Archives - {data.metadata.title}</title>
</svelte:head>

<div
	class="relative flex grow bg-[url('/assets/background.jpg')] bg-cover bg-scroll bg-center md:bg-fixed"
>
	<!-- Floating back button -->
	<a
		href={resolve('/')}
		aria-label="Go back"
		title="Go Back"
		class="fixed top-6 left-4 z-50 inline-flex cursor-pointer items-center justify-center rounded-full border border-border-main bg-surface/80 p-2.5 text-text-muted shadow-lg backdrop-blur-md transition-colors hover:border-accent hover:text-accent sm:top-8 sm:left-6"
	>
		<ArrowLeft class="h-5 w-5 sm:h-6 sm:w-6" />
	</a>

	<div class="flex grow items-center justify-center bg-bg-main/80 px-4 sm:px-6">
		<main class="flex w-full max-w-xl flex-col items-center text-center">
			<h1 class="text-2xl font-bold tracking-tight text-accent sm:text-3xl md:text-4xl">
				Download Archives
			</h1>
			<p class="mt-2 text-xs leading-relaxed text-text-secondary sm:text-sm">
				Carry the records of this story wherever you wander, fully available for offline reading.
			</p>

			<div class="mt-8 flex w-full flex-col gap-4 sm:mt-10">
				<!-- EPUB card -->
				<div
					class="flex flex-col items-start rounded-2xl border border-border-main bg-surface p-5 text-left shadow-lg transition-colors hover:border-accent/50 sm:p-6"
				>
					<span
						class="rounded-lg bg-accent/15 px-3 py-1 text-xs font-bold tracking-wider text-accent uppercase"
					>
						EPUB Format
					</span>
					<p class="mt-3 text-xs leading-relaxed text-text-secondary sm:text-sm">
						Flowing text tailored for e-readers and mobile apps. Ideal for comfortable, long reading
						sessions.
					</p>
					<a
						href="#"
						class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-xs font-bold text-bg-main shadow-md transition-colors hover:bg-accent-hover sm:py-3 sm:text-sm"
					>
						<Download class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
						<span>Download EPUB</span>
					</a>
				</div>

				<!-- PDF card -->
				<div
					class="flex flex-col items-start rounded-2xl border border-border-main bg-surface p-5 text-left shadow-lg transition-colors hover:border-accent/50 sm:p-6"
				>
					<span
						class="rounded-lg bg-accent/15 px-3 py-1 text-xs font-bold tracking-wider text-accent uppercase"
					>
						PDF Format
					</span>
					<p class="mt-3 text-xs leading-relaxed text-text-secondary sm:text-sm">
						Preserves the exact layout and typography. Best suited for desktops, laptops, and tablet
						displays.
					</p>
					<a
						href="#"
						class="mt-4 inline-flex w-full items-center justify-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-bold text-text-primary shadow-md transition-colors hover:border-accent-hover hover:bg-surface-hover sm:py-3 sm:text-sm"
					>
						<Download class="h-4 w-4 shrink-0 text-accent sm:h-5 sm:w-5" />
						<span>Download PDF</span>
					</a>
				</div>
			</div>
		</main>
	</div>
</div>
