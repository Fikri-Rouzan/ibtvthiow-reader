<script lang="ts">
	import { cubicOut } from 'svelte/easing';
	import { fly } from 'svelte/transition';
	import {
		DEFAULT_READER_SETTINGS,
		FONT_OPTIONS,
		type ReaderSettings,
		type ReaderTheme,
		type TextAlign
	} from '#lib/types/reader';
	import {
		TextAlignCenter,
		TextAlignJustify,
		TextAlignStart,
		TextAlignEnd,
		RotateCcw,
		ChevronDown,
		Check
	} from '@lucide/svelte';

	let {
		settings = $bindable()
	}: {
		settings: ReaderSettings;
	} = $props();

	// Dropdown open states
	let isThemeOpen = $state(false);
	let isFontOpen = $state(false);

	const THEMES: { id: ReaderTheme; label: string }[] = [
		{ id: 'catppuccin', label: 'Catppuccin' },
		{ id: 'dark', label: 'Dark' },
		{ id: 'dracula', label: 'Dracula' },
		{ id: 'emerald', label: 'Emerald' },
		{ id: 'gruvbox', label: 'Gruvbox' },
		{ id: 'light', label: 'Light' },
		{ id: 'midnight', label: 'Midnight' },
		{ id: 'nord', label: 'Nord' },
		{ id: 'rose-pine', label: 'Rosé Pine' },
		{ id: 'sepia', label: 'Sepia' }
	];

	const ALIGNMENTS: { id: TextAlign; label: string; icon: typeof TextAlignStart }[] = [
		{ id: 'left', label: 'Left', icon: TextAlignStart },
		{ id: 'center', label: 'Center', icon: TextAlignCenter },
		{ id: 'right', label: 'Right', icon: TextAlignEnd },
		{ id: 'justify', label: 'Justify', icon: TextAlignJustify }
	];

	// Derived current labels for custom dropdown display
	let currentThemeLabel = $derived(
		THEMES.find((t) => t.id === settings.theme)?.label ?? 'Dark Theme'
	);

	let currentFontName = $derived(
		FONT_OPTIONS.find((f) => f.family === settings.fontFamily)?.name ?? 'Default'
	);

	function toggleThemeDropdown() {
		isThemeOpen = !isThemeOpen;
		if (isThemeOpen) isFontOpen = false;
	}

	function toggleFontDropdown() {
		isFontOpen = !isFontOpen;
		if (isFontOpen) isThemeOpen = false;
	}

	function selectTheme(themeId: ReaderTheme) {
		settings.theme = themeId;
		isThemeOpen = false;
	}

	function selectFont(fontFamily: string) {
		settings.fontFamily = fontFamily;
		isFontOpen = false;
	}

	function resetToDefault() {
		settings = { ...DEFAULT_READER_SETTINGS };
		isThemeOpen = false;
		isFontOpen = false;
	}
</script>

<div class="space-y-5 text-xs sm:text-sm">
	<!-- Color theme dropdown -->
	<div class="relative space-y-1.5">
		<span class="text-xs font-semibold tracking-wider text-text-muted uppercase">Color Theme</span>
		<button
			type="button"
			onclick={toggleThemeDropdown}
			aria-expanded={isThemeOpen}
			aria-haspopup="listbox"
			class="flex w-full cursor-pointer items-center justify-between rounded-lg border border-border-main bg-surface px-3 py-2.5 text-xs text-text-primary transition-colors hover:border-accent focus:border-accent focus:outline-none sm:text-sm"
		>
			<span>{currentThemeLabel}</span>
			<ChevronDown
				class="h-4 w-4 text-text-muted transition-transform duration-200 {isThemeOpen
					? 'rotate-180 text-accent'
					: ''}"
			/>
		</button>

		{#if isThemeOpen}
			<div
				role="listbox"
				transition:fly={{ y: -6, duration: 250, easing: cubicOut }}
				class="absolute top-full right-0 left-0 z-20 mt-1 max-h-56 overflow-y-auto rounded-lg border border-border-main bg-surface p-1 shadow-xl backdrop-blur-md"
			>
				{#each THEMES as t (t.id)}
					{@const isSelected = settings.theme === t.id}
					<button
						type="button"
						role="option"
						aria-selected={isSelected}
						onclick={() => selectTheme(t.id)}
						class="flex w-full cursor-pointer items-center justify-between rounded-md px-3 py-2 text-xs transition-colors hover:bg-surface-hover hover:text-text-primary sm:text-sm {isSelected
							? 'bg-surface-hover font-semibold text-accent'
							: 'text-text-secondary'}"
					>
						<span>{t.label}</span>
						{#if isSelected}
							<Check class="h-4 w-4 text-accent" />
						{/if}
					</button>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Font family dropdown -->
	<div class="relative space-y-1.5">
		<span class="text-xs font-semibold tracking-wider text-text-muted uppercase">Font Family</span>
		<button
			type="button"
			onclick={toggleFontDropdown}
			aria-expanded={isFontOpen}
			aria-haspopup="listbox"
			class="flex w-full cursor-pointer items-center justify-between rounded-lg border border-border-main bg-surface px-3 py-2.5 text-xs text-text-primary transition-colors hover:border-accent focus:border-accent focus:outline-none sm:text-sm"
		>
			<span style="font-family: {settings.fontFamily}">{currentFontName}</span>
			<ChevronDown
				class="h-4 w-4 text-text-muted transition-transform duration-200 {isFontOpen
					? 'rotate-180 text-accent'
					: ''}"
			/>
		</button>

		{#if isFontOpen}
			<div
				role="listbox"
				transition:fly={{ y: -6, duration: 250, easing: cubicOut }}
				class="absolute top-full right-0 left-0 z-20 mt-1 max-h-60 overflow-y-auto rounded-lg border border-border-main bg-surface p-1 shadow-xl backdrop-blur-md"
			>
				{#each FONT_OPTIONS as font (font.id)}
					{@const isSelected = settings.fontFamily === font.family}
					<button
						type="button"
						role="option"
						aria-selected={isSelected}
						onclick={() => selectFont(font.family)}
						class="flex w-full cursor-pointer items-center justify-between rounded-md px-3 py-2 text-xs transition-colors hover:bg-surface-hover hover:text-text-primary sm:text-sm {isSelected
							? 'bg-surface-hover font-semibold text-accent'
							: 'text-text-secondary'}"
					>
						<span style="font-family: {font.family}">
							{font.name} <span class="text-[10px] text-text-muted">({font.category})</span>
						</span>
						{#if isSelected}
							<Check class="h-4 w-4 text-accent" />
						{/if}
					</button>
				{/each}
			</div>
		{/if}
	</div>

	<!-- Font size slider -->
	<div class="space-y-1.5">
		<div class="flex items-center justify-between">
			<span class="text-xs font-semibold tracking-wider text-text-muted uppercase">Font Size</span>
			<span class="font-mono text-xs font-bold text-accent sm:text-sm">{settings.fontSize}px</span>
		</div>
		<input
			type="range"
			min="14"
			max="28"
			step="1"
			bind:value={settings.fontSize}
			class="w-full cursor-pointer accent-accent"
		/>
	</div>

	<!-- Line height slider -->
	<div class="space-y-1.5">
		<div class="flex items-center justify-between">
			<span class="text-xs font-semibold tracking-wider text-text-muted uppercase">Line Height</span
			>
			<span class="font-mono text-xs font-bold text-accent sm:text-sm">{settings.lineHeight}</span>
		</div>
		<input
			type="range"
			min="1.4"
			max="2.4"
			step="0.1"
			bind:value={settings.lineHeight}
			class="w-full cursor-pointer accent-accent"
		/>
	</div>

	<!-- Font weight slider -->
	<div class="space-y-1.5">
		<div class="flex items-center justify-between">
			<span class="text-xs font-semibold tracking-wider text-text-muted uppercase">Font Weight</span
			>
			<span class="font-mono text-xs font-bold text-accent sm:text-sm">{settings.fontWeight}</span>
		</div>
		<input
			type="range"
			min="400"
			max="700"
			step="100"
			bind:value={settings.fontWeight}
			class="w-full cursor-pointer accent-accent"
		/>
	</div>

	<!-- Text alignment selector -->
	<div class="space-y-1.5">
		<span class="text-xs font-semibold tracking-wider text-text-muted uppercase"
			>Text Alignment</span
		>
		<div class="grid grid-cols-4 gap-2">
			{#each ALIGNMENTS as align (align.id)}
				{@const Icon = align.icon}
				{@const isSelected = settings.textAlign === align.id}
				<button
					type="button"
					onclick={() => (settings.textAlign = align.id)}
					aria-label={align.label}
					title={align.label}
					class="flex cursor-pointer items-center justify-center rounded-lg border p-2 transition-colors {isSelected
						? 'border-accent bg-accent font-bold text-bg-main shadow-sm'
						: 'border-border-main bg-surface text-text-secondary hover:bg-surface-hover hover:text-text-primary'}"
				>
					<Icon class="h-4 w-4" />
				</button>
			{/each}
		</div>
	</div>

	<!-- Reset to default button -->
	<div class="border-t border-border-main pt-4">
		<button
			type="button"
			onclick={resetToDefault}
			class="inline-flex w-full cursor-pointer items-center justify-center gap-2 rounded-xl border border-accent bg-surface px-4 py-2.5 text-xs font-semibold text-text-primary shadow-sm transition-colors hover:border-accent-hover hover:bg-surface-hover sm:py-3 sm:text-sm"
		>
			<RotateCcw class="h-4 w-4 shrink-0 text-accent sm:h-5 sm:w-5" />
			<span>Reset to Default</span>
		</button>
	</div>
</div>
