/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'display': ['Playfair Display', 'serif'],
      },
      colors: {
        forest: {
          50: '#f0f5f0',
          100: '#dde8dc',
          200: '#bdd1bc',
          300: '#97b596',
          400: '#729871',
          500: '#557d54',
          600: '#426342',
          700: '#365036',
          800: '#2d422d',
          900: '#263826',
          950: '#131f13',
        },
      },
    },
  },
  plugins: [],
};
