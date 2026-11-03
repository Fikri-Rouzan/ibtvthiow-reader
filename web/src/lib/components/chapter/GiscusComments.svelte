<script lang="ts">
	import { page } from '$app/state';
	import { giscusAction } from '#lib/actions/giscus';
	import { getCommentCount } from '#lib/services/giscusService';
	import type { ReaderTheme } from '#lib/types/reader';
	import { ChevronDown, MessageSquare } from '@lucide/svelte';

	let {
		term = '',
		theme = 'dark'
	}: {
		term?: string;
		theme?: ReaderTheme;
	} = $props();

	let showComments = $state(false);
	let commentCount = $state<number | null>(null);

	// Fetch comment count asynchronously whenever term changes
	$effect(() => {
		if (term) {
			getCommentCount(term).then((count) => {
				commentCount = count;
			});
		}
	});

	// Derive absolute origin URL for CSS endpoint
	let siteOrigin = $derived(page.url.origin);

	// Direct all themes to the dynamic server endpoint
	let giscusTheme = $derived(`${siteOrigin}/giscus-theme.css?theme=${theme}`);
</script>

{#if term}
	<section
		id="comments-section"
		class="mt-8 space-y-4 sm:mt-10"
		aria-label="Chapter discussion comments"
	>
		<!-- Toggle comments button -->
		<div class="flex flex-col items-center justify-center">
			<button
				type="button"
				onclick={() => (showComments = !showComments)}
				class="inline-flex cursor-pointer items-center justify-center gap-2.5 rounded-xl bg-accent px-6 py-3 text-xs font-bold text-bg-main shadow-md transition-colors hover:bg-accent-hover sm:px-7 sm:py-3.5 sm:text-sm"
			>
				<MessageSquare class="h-4 w-4 shrink-0 sm:h-5 sm:w-5" />
				<span>
					{showComments ? 'Hide Comments' : 'Show Comments'}
					{#if commentCount !== null}
						({commentCount})
					{/if}
				</span>
				<ChevronDown
					class="h-4 w-4 shrink-0 transition-transform duration-300 sm:h-5 sm:w-5 {showComments
						? 'rotate-180'
						: ''}"
				/>
			</button>
		</div>

		<!-- Giscus -->
		{#if showComments}
			<div
				use:giscusAction={{ term, theme: giscusTheme }}
				class="giscus-wrapper min-h-45 w-full pt-4"
			></div>
		{/if}
	</section>
{/if}
