<script lang="ts">
	import type { Token } from 'marked';
	import { asset } from '$app/paths';
	import InlineRenderer from './InlineRenderer.svelte';

	let { tokens = [] }: { tokens?: Token[] } = $props();
</script>

{#each tokens as token, idx (`inline-${token.type}-${idx}`)}
	{#if token.type === 'text'}
		{#if 'tokens' in token && token.tokens && token.tokens.length > 0}
			<InlineRenderer tokens={token.tokens} />
		{:else}
			{token.text}
		{/if}
	{:else if token.type === 'strong'}
		<strong>
			<InlineRenderer tokens={token.tokens} />
		</strong>
	{:else if token.type === 'em'}
		<em>
			<InlineRenderer tokens={token.tokens} />
		</em>
	{:else if token.type === 'codespan'}
		<code>{token.text}</code>
	{:else if token.type === 'br'}
		<br />
	{:else if token.type === 'escape'}
		{token.text}
	{:else if token.type === 'image'}
		<img
			src={asset(token.href.replace(/^\//, ''))}
			alt={token.text}
			title={token.title || undefined}
			class="mx-auto my-6 block max-h-100 w-auto rounded-xl border border-border-main object-contain shadow-lg sm:max-h-150 md:max-h-190"
			loading="lazy"
		/>
	{/if}
{/each}
