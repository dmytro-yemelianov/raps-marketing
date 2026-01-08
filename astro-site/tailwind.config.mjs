/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        'raps-blue': '#667eea',
        'raps-purple': '#764ba2',
        'raps-green': '#28a745',
        'raps-gray': '#6c757d',
        'raps-light': '#f8f9fa',
        'raps-dark': '#343a40',
        'raps-error': '#dc3545',
        'raps-warning': '#ffc107',
        'aps-primary': '#0696d7',
        'aps-secondary': '#fdb714',
        'aps-dark': '#1a1a1a',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Consolas', 'Monaco', 'monospace'],
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            'code::before': {
              content: '""',
            },
            'code::after': {
              content: '""',
            },
            code: {
              backgroundColor: theme('colors.gray.100'),
              padding: '0.25rem',
              borderRadius: '0.25rem',
              fontWeight: '400',
            },
            'pre code': {
              backgroundColor: 'transparent',
              padding: '0',
            },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}