<script lang="ts">
	import type { Token } from 'marked';
	import InlineRenderer from './InlineRenderer.svelte';

	let { tokens = [] }: { tokens?: Token[] } = $props();
</script>

<div class="space-y-4 text-text-secondary sm:space-y-5">
	{#each tokens as token, idx (`block-${token.type}-${idx}`)}
		{#if token.type === 'paragraph'}
			<p class="text-sm leading-relaxed sm:text-base md:text-lg md:leading-loose">
				<InlineRenderer tokens={token.tokens} />
			</p>
		{:else if token.type === 'heading'}
			{#if token.depth === 1}
				<h1 class="text-xl font-bold text-text-primary sm:text-2xl md:text-3xl">
					<InlineRenderer tokens={token.tokens} />
				</h1>
			{:else if token.depth === 2}
				<h2 class="text-lg font-bold text-text-primary sm:text-xl md:text-2xl">
					<InlineRenderer tokens={token.tokens} />
				</h2>
			{:else if token.depth === 3}
				<h3 class="text-base font-bold text-text-primary sm:text-lg md:text-xl">
					<InlineRenderer tokens={token.tokens} />
				</h3>
			{:else}
				<h4 class="text-sm font-bold text-text-primary sm:text-base md:text-lg">
					<InlineRenderer tokens={token.tokens} />
				</h4>
			{/if}
		{:else if token.type === 'hr'}
			<hr class="my-6 border-border-main sm:my-8" />
		{:else if token.type === 'blockquote'}
			<blockquote
				class="border-l-4 border-accent pl-4 text-xs text-text-muted italic sm:text-sm md:text-base"
			>
				{#if token.tokens}
					<InlineRenderer tokens={token.tokens} />
				{/if}
			</blockquote>
		{/if}
	{/each}
</div>
