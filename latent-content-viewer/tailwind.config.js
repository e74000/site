/** @type {import('tailwindcss').Config} */
const colors = {
  background: '#1c1c1c',
  foreground: '#f7f6ec',
  cursor: '#eccf4f',
  selectionBackground: '#165776',
  color0: '#343835',
  color8: '#585a58',
  color1: '#ce3e60',
  color9: '#722235',
  color2: '#7bb75b',
  color10: '#767e2b',
  color3: '#e8b32a',
  color11: '#77592e',
  color4: '#4c99d3',
  color12: '#135879',
  color5: '#a57fc4',
  color13: '#5f4190',
  color6: '#389aac',
  color14: '#19444c',
  color7: '#f9faf6',
  color15: '#b1b5ae',
  selectionForeground: '#1c1c1c'
};

module.exports = {
  content: [
    './index.html',
    './src/**/*.{svelte,js,ts}',
  ],
  theme: {
    extend: {
      colors: {
        background: colors.background,
        foreground: colors.foreground,
        cursor: colors.cursor,
        selectionBackground: colors.selectionBackground,
        color0: colors.color0,
        color8: colors.color8,
        color1: colors.color1,
        color9: colors.color9,
        color2: colors.color2,
        color10: colors.color10,
        color3: colors.color3,
        color11: colors.color11,
        color4: colors.color4,
        color12: colors.color12,
        color5: colors.color5,
        color13: colors.color13,
        color6: colors.color6,
        color14: colors.color14,
        color7: colors.color7,
        color15: colors.color15,
        selectionForeground: colors.selectionForeground
      },
    },
  },
  plugins: [],
}
