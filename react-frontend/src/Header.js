import React, {useState} from "react";

import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import IconButton from '@mui/material/IconButton';
import InfoIcon from "@mui/icons-material/Info";
import Typography from "@mui/material/Typography";

function Header(props) {
  const [isDarkMode, setIsDarkMode] = useState(false);
  return (
    <div>
      <Grid container spacing={2} justifyContent="space-between" alignItems="center">
        <Grid item>
          <Typography variant="h3" style={{ margin: "30px 0" }}>
            Prolog testing system
          </Typography>
        </Grid>
        <Grid item>
          <Grid container spacing={2} justifyContent="center" alignItems={"center"}>
            <Grid item>
              <IconButton
                sx={{ ml: 1 }}
                color="inherit"
                onClick={() => {
                  props.switchTheme()
                  setIsDarkMode((prevIsDarkMode) => { return !prevIsDarkMode; })
                }}
                >
                { isDarkMode ? <Brightness7Icon /> : <Brightness4Icon /> }
              </IconButton>
            </Grid>
            <Grid item>
              <Button
                variant="text"
                startIcon={<InfoIcon />}
                href="https://github.com/m-danya/prolog-testing-system"
                target="_blank"
                >
                О проекте
              </Button>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </div>
  );
}

export default Header;
