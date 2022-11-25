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
      'sans': ['Samsung Sans Regular', 'sans-serif'],
    },
    extend: {
      backgroundImage: {
        'main': "radial-gradient(circle, #8093ff, #7581fa, #6d6ff5, #675bee, #6445e5);",
      }
    },
  },
  plugins: [],
}
