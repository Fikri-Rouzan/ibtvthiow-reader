import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from '@lucide/svelte';

export type PaginationItem = number | '...';

export interface NavButtonConfig {
	id: string;
	icon: typeof ChevronLeft;
	title: string;
	targetPage: (current: number, total: number) => number;
	disabled: (current: number, total: number) => boolean;
}

// Common button classnames
export const NAV_BTN_CLASS =
	'inline-flex h-7 w-7 cursor-pointer items-center justify-center rounded-md border border-border-main bg-surface text-text-muted transition-colors hover:bg-surface-hover disabled:cursor-not-allowed disabled:opacity-30 sm:h-8 sm:w-8';

// Left navigation buttons configuration (First & Previous)
export const NAV_BUTTONS_LEFT: NavButtonConfig[] = [
	{
		id: 'first',
		icon: ChevronsLeft,
		title: 'First Page',
		targetPage: () => 1,
		disabled: (current: number) => current === 1
	},
	{
		id: 'prev',
		icon: ChevronLeft,
		title: 'Previous Page',
		targetPage: (current: number) => current - 1,
		disabled: (current: number) => current === 1
	}
];

// Right navigation buttons configuration (Next & Last)
export const NAV_BUTTONS_RIGHT: NavButtonConfig[] = [
	{
		id: 'next',
		icon: ChevronRight,
		title: 'Next Page',
		targetPage: (current: number) => current + 1,
		disabled: (current: number, total: number) => current === total
	},
	{
		id: 'last',
		icon: ChevronsRight,
		title: 'Last Page',
		targetPage: (_: number, total: number) => total,
		disabled: (current: number, total: number) => current === total
	}
];

/**
 * Generate pagination sequence with ellipses for large page sets.
 */
export function getPaginationItems(currentPage: number, totalPages: number): PaginationItem[] {
	if (totalPages <= 5) {
		return Array.from({ length: totalPages }, (_, i) => i + 1);
	}

	// Near the beginning
	if (currentPage <= 2) {
		return [1, 2, 3, '...', totalPages];
	}

	// Near the end
	if (currentPage >= totalPages - 1) {
		return [1, '...', totalPages - 2, totalPages - 1, totalPages];
	}

	// Middle pages
	return [1, '...', currentPage, '...', totalPages];
}
