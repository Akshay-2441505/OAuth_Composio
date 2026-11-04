/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        dark: {
          bg: '#0A0E17',        // Deep modern midnight slate
          sidebar: '#0E1321',   // Refined distinct sidebar
          surface: '#141C2E',   // Card surface with clear depth
          elevated: '#1B253D',  // Elevated interactive wells / sub-cards
          card: '#141C2E',
          hover: '#222F4C',     // Clear interactive hover
        },
        border: {
          subtle: '#212D45',    // Soft, elegant border
          DEFAULT: '#2D3D5E',
          muted: '#182236',
          accent: 'rgba(163, 230, 53, 0.45)',
        },
        content: {
          primary: '#FFFFFF',
          secondary: '#CBD5E1', // High-contrast readable body text (Slate-300)
          muted: '#94A3B8',     // High-contrast readable secondary text (Slate-400)
        },
        accent: {
          DEFAULT: '#A3E635',   // Crisp, professional lime
          hover: '#BEF264',
          dim: 'rgba(163, 230, 53, 0.12)',
          border: 'rgba(163, 230, 53, 0.40)',
          glow: 'rgba(163, 230, 53, 0.20)',
        },
      },
      fontFamily: {
        sans: ['Geist', 'Inter', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['Geist Mono', 'JetBrains Mono', 'Menlo', 'Monaco', 'Courier New', 'monospace'],
      },
    },
  },
  plugins: [],
}
