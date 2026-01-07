/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        raps: {
          blue: '#667eea',
          purple: '#764ba2',
          green: '#28a745',
          gray: '#6c757d',
          light: '#f8f9fa',
          dark: '#343a40',
          error: '#dc3545',
          warning: '#ffc107',
        },
        aps: {
          primary: '#0696d7',
          secondary: '#fdb714',
          dark: '#1a1a1a',
        },
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