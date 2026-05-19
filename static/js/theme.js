/**
 * theme.js — Dark / light mode manager
 * Exports: initTheme(), toggleTheme()
 */

const STORAGE_KEY = 'acadbot-theme';

/**
 * Apply a theme ('light' | 'dark') to the document and update the toggle button.
 * @param {string} theme
 */
export function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem(STORAGE_KEY, theme);

  // Update any toggle buttons that exist on the page
  document.querySelectorAll('.btn-theme').forEach((btn) => {
    btn.textContent = theme === 'dark' ? '☀️' : '🌙';
  });
}

/**
 * Toggle between light and dark.
 */
export function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') ?? 'light';
  applyTheme(current === 'dark' ? 'light' : 'dark');
}

/**
 * Initialise theme on page load, reading from localStorage.
 */
export function initTheme() {
  const saved = localStorage.getItem(STORAGE_KEY) ?? 'light';
  applyTheme(saved);
}
