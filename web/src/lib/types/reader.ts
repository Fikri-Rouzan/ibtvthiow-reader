export type ReaderTheme =
	| 'dark'
	| 'light'
	| 'sepia'
	| 'nord'
	| 'dracula'
	| 'catppuccin'
	| 'midnight'
	| 'emerald'
	| 'gruvbox'
	| 'rose-pine';
export type TextAlign = 'left' | 'center' | 'right' | 'justify';
export type DrawerType = 'chapters' | 'settings' | null;

export interface FontOption {
	id: string;
	name: string;
	family: string;
	category: 'Sans' | 'Serif' | 'Mono';
}

export interface ReaderSettings {
	theme: ReaderTheme;
	fontSize: number;
	fontFamily: string;
	lineHeight: number;
	fontWeight: number;
	textAlign: TextAlign;
}

export const FONT_OPTIONS: FontOption[] = [
	{ id: 'garamond', name: 'EB Garamond', family: "'EB Garamond', serif", category: 'Serif' },
	{ id: 'inter', name: 'Inter', family: "'Inter', sans-serif", category: 'Sans' },
	{
		id: 'jetbrains',
		name: 'JetBrains Mono',
		family: "'JetBrains Mono', monospace",
		category: 'Mono'
	},
	{ id: 'literata', name: 'Literata', family: "'Literata', serif", category: 'Serif' },
	{ id: 'lora', name: 'Lora', family: "'Lora', serif", category: 'Serif' },
	{ id: 'merriweather', name: 'Merriweather', family: "'Merriweather', serif", category: 'Serif' },
	{ id: 'nunito', name: 'Nunito', family: "'Nunito', sans-serif", category: 'Sans' },
	{
		id: 'jakarta',
		name: 'Plus Jakarta Sans',
		family: "'Plus Jakarta Sans', sans-serif",
		category: 'Sans'
	},
	{ id: 'roboto-serif', name: 'Roboto Serif', family: "'Roboto Serif', serif", category: 'Serif' },
	{
		id: 'source-serif',
		name: 'Source Serif 4',
		family: "'Source Serif 4', serif",
		category: 'Serif'
	}
];

export const DEFAULT_READER_SETTINGS: ReaderSettings = {
	theme: 'dark',
	fontSize: 18,
	fontFamily: "'Plus Jakarta Sans', sans-serif",
	lineHeight: 1.7,
	fontWeight: 400,
	textAlign: 'left'
};
