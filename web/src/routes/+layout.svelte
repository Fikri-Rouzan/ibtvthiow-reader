<script lang="ts">
	import './layout.css';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();
</script>

<div class="flex min-h-screen flex-col bg-bg-main font-sans text-text-primary antialiased">
	{@render children()}
</div>
