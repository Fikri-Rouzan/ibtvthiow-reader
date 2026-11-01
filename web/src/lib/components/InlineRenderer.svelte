<script lang="ts">
	import type { Token } from 'marked';
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
	{/if}
{/each}
