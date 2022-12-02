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
        'main': '#fffffe',
        'background': '#d8eefe',
        'paraf': '#5f6c7b',
        'highlight': '#3da9fc',
        'secondary': '#90b4ce',
        'headline': '#094067',
        'tertiary': '#ef4565',
      }
    }
  },
  plugins: [],
}
