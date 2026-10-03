/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/*.py",
    "./apps/**/*.html",
    "./static/**/*.js",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f0f7ff',
          100: '#e0effe',
          200: '#bae0fd',
          300: '#7cc8fc',
          400: '#36aff7',
          500: '#0c94e8',
          600: '#0076c6',
          700: '#005ea2',
          800: '#055085',
          900: '#0a436f',
          950: '#072b49',
        },
        dark: {
          bg: '#0B0F17',
          card: '#131926',
          border: '#1E293B',
          muted: '#64748B',
          accent: '#38BDF8',
          gradientFrom: '#0F172A',
          gradientTo: '#1E1B4B'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
