import type { RequestHandler } from './$types';
import type { ReaderTheme } from '#lib/types/reader';

export const prerender = false;

interface ThemeColorSpec {
	bg: string;
	surface: string;
	border: string;
	textPrimary: string;
	textSecondary: string;
	textMuted: string;
	accent: string;
	accentHover: string;
	btnText: string;
}

const THEME_MAP: Record<ReaderTheme, ThemeColorSpec> = {
	dark: {
		bg: '#0b0e14',
		surface: '#151a26',
		border: 'rgba(255, 255, 255, 0.1)',
		textPrimary: '#f8fafc',
		textSecondary: '#cbd5e1',
		textMuted: '#64748b',
		accent: '#f59e0b',
		accentHover: '#d97706',
		btnText: '#0b0e14'
	},
	light: {
		bg: '#ffffff',
		surface: '#f4f4f5',
		border: 'rgba(0, 0, 0, 0.1)',
		textPrimary: '#18181b',
		textSecondary: '#3f3f46',
		textMuted: '#71717a',
		accent: '#d97706',
		accentHover: '#b45309',
		btnText: '#ffffff'
	},
	sepia: {
		bg: '#f4ecd8',
		surface: '#ebe1cb',
		border: 'rgba(67, 52, 34, 0.15)',
		textPrimary: '#433422',
		textSecondary: '#5f4b32',
		textMuted: '#7c6853',
		accent: '#c2410c',
		accentHover: '#9a3412',
		btnText: '#ffffff'
	},
	nord: {
		bg: '#2e3440',
		surface: '#2b313d',
		border: 'rgba(216, 222, 233, 0.15)',
		textPrimary: '#eceff4',
		textSecondary: '#e5e9f0',
		textMuted: '#d8dee9',
		accent: '#88c0d0',
		accentHover: '#81a1c1',
		btnText: '#2e3440'
	},
	dracula: {
		bg: '#282a36',
		surface: '#343746',
		border: 'rgba(248, 248, 242, 0.15)',
		textPrimary: '#f8f8f2',
		textSecondary: '#e2e2dc',
		textMuted: '#6272a4',
		accent: '#bd93f9',
		accentHover: '#a371f7',
		btnText: '#282a36'
	},
	catppuccin: {
		bg: '#1e1e2e',
		surface: '#313244',
		border: 'rgba(205, 214, 244, 0.15)',
		textPrimary: '#cdd6f4',
		textSecondary: '#bac2de',
		textMuted: '#7f849c',
		accent: '#cba6f7',
		accentHover: '#b4befe',
		btnText: '#1e1e2e'
	},
	midnight: {
		bg: '#000000',
		surface: '#18181b',
		border: 'rgba(255, 255, 255, 0.12)',
		textPrimary: '#f4f4f5',
		textSecondary: '#a1a1aa',
		textMuted: '#71717a',
		accent: '#38bdf8',
		accentHover: '#0284c7',
		btnText: '#000000'
	},
	emerald: {
		bg: '#061a14',
		surface: '#0b2b21',
		border: 'rgba(167, 243, 208, 0.15)',
		textPrimary: '#ecfdf5',
		textSecondary: '#a7f3d0',
		textMuted: '#34d399',
		accent: '#10b981',
		accentHover: '#059669',
		btnText: '#061a14'
	},
	gruvbox: {
		bg: '#282828',
		surface: '#3c3836',
		border: 'rgba(235, 219, 178, 0.15)',
		textPrimary: '#ebdbb2',
		textSecondary: '#d5c4a1',
		textMuted: '#928374',
		accent: '#fe8019',
		accentHover: '#d65d0e',
		btnText: '#282828'
	},
	'rose-pine': {
		bg: '#191724',
		surface: '#1f1d2e',
		border: 'rgba(224, 222, 244, 0.15)',
		textPrimary: '#e0def4',
		textSecondary: '#c4a7e7',
		textMuted: '#908caa',
		accent: '#ebbcba',
		accentHover: '#d7827e',
		btnText: '#191724'
	}
};

/**
 * Generates custom Primer CSS overrides for Giscus iframe.
 */
function generateGiscusCss(themeKey: string): string {
	const t = THEME_MAP[themeKey as ReaderTheme] || THEME_MAP.dark;

	return `
		main {
			--color-canvas-default: ${t.bg} !important;
			--color-canvas-overlay: ${t.surface} !important;
			--color-canvas-subtle: ${t.surface} !important;
			--color-border-default: ${t.border} !important;
			--color-border-muted: ${t.border} !important;
			--color-fg-default: ${t.textPrimary} !important;
			--color-fg-muted: ${t.textMuted} !important;
			--color-fg-subtle: ${t.textSecondary} !important;
			--color-accent-fg: ${t.accent} !important;
			--color-accent-emphasis: ${t.accentHover} !important;

			--color-btn-text: ${t.btnText} !important;
			--color-btn-bg: ${t.accent} !important;
			--color-btn-border: ${t.accent} !important;
			--color-btn-hover-bg: ${t.accentHover} !important;
			--color-btn-hover-border: ${t.accentHover} !important;

			--color-btn-primary-text: ${t.btnText} !important;
			--color-btn-primary-bg: ${t.accent} !important;
			--color-btn-primary-border: ${t.accent} !important;
			--color-btn-primary-hover-bg: ${t.accentHover} !important;
			--color-btn-primary-hover-border: ${t.accentHover} !important;
		}

		.gsc-comment-box,
		.gsc-timeline-comment,
		.gsc-reply-box,
		.gsc-header {
			background-color: ${t.surface} !important;
			border-color: ${t.border} !important;
		}

		.gsc-comment-box-textarea,
		.gsc-comment-box-textarea:focus {
			background-color: ${t.bg} !important;
			color: ${t.textPrimary} !important;
			border-color: ${t.border} !important;
		}

		.gsc-comment-box-textarea::placeholder {
			color: ${t.textMuted} !important;
		}

		.gsc-comment-box-bottom,
		.gsc-comment-header,
		.gsc-comment-footer {
			background-color: transparent !important;
			border-color: ${t.border} !important;
		}
	`;
}

export const GET: RequestHandler = ({ url }) => {
	const themeParam = url.searchParams.get('theme') || 'dark';
	const cssContent = generateGiscusCss(themeParam);

	return new Response(cssContent, {
		headers: {
			'Content-Type': 'text/css; charset=utf-8',
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET, OPTIONS',
			'Cache-Control': 'public, max-age=3600'
		}
	});
};

export const OPTIONS: RequestHandler = () => {
	return new Response(null, {
		headers: {
			'Access-Control-Allow-Origin': '*',
			'Access-Control-Allow-Methods': 'GET, OPTIONS',
			'Access-Control-Allow-Headers': 'Content-Type'
		}
	});
};
