import { createTheme } from '@mui/material/styles';

let lightTheme = createTheme({
  palette: {
    mode: 'light',
  },
});

lightTheme.typography.h3 = {
  ...lightTheme.typography.h3,
  fontSize: '1.0rem',
  '@media (min-width:500px)': {
    fontSize: '1.5rem',
  },
  [lightTheme.breakpoints.up('md')]: {
    fontSize: '3.0rem',
  },
};


let darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

darkTheme.typography.h3 = {
  ...darkTheme.typography.h3,
  fontSize: '1.0rem',
  '@media (min-width:500px)': {
    fontSize: '1.5rem',
  },
  [darkTheme.breakpoints.up('md')]: {
    fontSize: '3.0rem',
  },
};

export { lightTheme, darkTheme };
