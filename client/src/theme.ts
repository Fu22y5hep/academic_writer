import { createTheme, rem } from '@mantine/core';

export const theme = createTheme({
  colorScheme: 'light',
  primaryColor: 'blue',
  defaultRadius: 'md',
  fontFamily: 'Inter, sans-serif',
  headings: {
    fontFamily: 'Inter, sans-serif',
    sizes: {
      h1: { fontSize: rem(40) },
      h2: { fontSize: rem(32) },
      h3: { fontSize: rem(24) },
      h4: { fontSize: rem(20) },
      h5: { fontSize: rem(18) },
      h6: { fontSize: rem(16) },
    },
  },
  components: {
    Button: {
      defaultProps: {
        size: 'md',
      },
      styles: {
        root: {
          fontWeight: 600,
        },
      },
    },
    Input: {
      defaultProps: {
        size: 'md',
      },
    },
    NavLink: {
      styles: {
        root: {
          '&[data-active]': {
            backgroundColor: 'var(--mantine-color-blue-light)',
            color: 'var(--mantine-color-blue-filled)',
          },
        },
      },
    },
  },
});
