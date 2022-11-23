/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
      './templates/*.html',
      './static/js/*.js',
      './static/css/src/*.css',
    ],
  },
  theme: {
    fontFamily: {
      'sans': ['Call_Duty', 'sans-serif'],
    },
    extend: {
      backgroundImage: {
        'main': "linear-gradient(to bottom, #d8eefe, #c2e4fd, #abd9fb, #93cffa, #79c4f9)",
      }
    },
  },
  plugins: [],
}
