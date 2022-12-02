/** @type {import('tailwindcss').Config} */
module.exports = {
  content: {
    relative: true,
    files: [
      './templates/*.html',
      './static/js/*.js',
      './static/css/src/*.css',
    ]
  },
  theme: {
    fontFamily: {
      'sans': ['Samsung Sans Regular', 'sans-serif'],
    },
    extend: {
      colors: {
        'background': '#D8EEFE',
      }
    }
  },
  plugins: [],
}
