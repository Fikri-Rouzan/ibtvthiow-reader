<script lang="ts">
	import { resolve } from '$app/paths';
	import { BookOpen, Download } from '@lucide/svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<svelte:head>
	<title>{data.metadata.title}</title>
</svelte:head>

<div
	class="relative flex grow bg-[url('/assets/background.jpg')] bg-cover bg-scroll bg-center md:bg-fixed"
>
	<div class="flex grow items-center justify-center bg-bg-main/80 px-4 sm:px-6">
		<div class="flex max-w-3xl flex-col items-center text-center">
			<blockquote
				class="mb-6 text-sm leading-relaxed font-medium text-text-secondary italic sm:mb-8 sm:text-lg md:text-xl"
			>
				&ldquo;Even as a villain, I couldn't bring myself to kill innocent people, so instead, I
				went around taking down other villains. Because Stardust, the hero, has always been my
				all-time favorite character. I didn't want her to struggle too much.&rdquo;
			</blockquote>

			<div class="flex flex-row items-center justify-center gap-2.5 sm:gap-4">
				<a
					href={resolve('/ibtvthiow')}
					class="inline-flex items-center justify-center gap-2 rounded-xl bg-accent px-4 py-2.5 text-xs font-semibold text-bg-main shadow-lg transition-colors hover:bg-accent-hover sm:px-6 sm:py-3.5 sm:text-base"
				>
					<BookOpen class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
					<span>Read Novel</span>
				</a>
				<a
					href={resolve('/download')}
					class="inline-flex items-center justify-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-lg transition-colors hover:border-accent-hover hover:bg-surface-hover sm:px-6 sm:py-3.5 sm:text-base"
				>
					<Download class="h-4 w-4 shrink-0 text-accent sm:h-5 sm:w-5" />
					<span>Download</span>
				</a>
			</div>
		</div>
	</div>
</div>
