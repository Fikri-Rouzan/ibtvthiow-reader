<script lang="ts">
	import { resolve } from '$app/paths';
	import type { ChapterItem } from '#lib/types/novel';

	let {
		chapters,
		lastReadSlug = null
	}: {
		chapters: ChapterItem[];
		lastReadSlug?: string | null;
	} = $props();
</script>

<div class="flex flex-col gap-2 border-t border-border-main pt-3 sm:pt-4">
	{#each chapters as chapter (chapter.slug)}
		{@const isLastRead = chapter.slug === lastReadSlug}
		<a
			href={resolve('/ibtvthiow/chapter/[slug]', { slug: chapter.slug })}
			class="group flex items-center justify-between rounded-lg px-3.5 py-2.5 text-xs transition-colors hover:border-accent-hover hover:bg-accent/40 hover:text-bg-main sm:px-4 sm:py-3 sm:text-sm {isLastRead
				? 'border border-last-read-border bg-last-read font-semibold text-accent'
				: 'border border-border-main bg-surface text-text-secondary'}"
		>
			<span class="truncate font-medium transition-colors group-hover:text-text-primary">
				{chapter.title}
			</span>
		</a>
	{/each}
</div>
