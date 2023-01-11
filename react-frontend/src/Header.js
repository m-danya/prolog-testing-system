import React from "react";

import Button from "@mui/material/Button";
import FormControl from "@mui/material/FormControl";
import Grid from "@mui/material/Grid";
import InfoIcon from "@mui/icons-material/Info";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import Typography from "@mui/material/Typography";

class Header extends React.Component {
  render() {
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
                <div style={{ width: "200px", maxWidth: "200px" }}>
                  <FormControl fullWidth>
                    <InputLabel id="theme-selector-label">Тема</InputLabel>
                    <Select
                      labelId="theme-selector-label"
                      label="Тема"
                      width="400px"
                      value={ this.props.selectedThemeName }
                      onChange={ this.props.setSelectedTheme }
                      >
                      <MenuItem value="lightTheme">Светлая</MenuItem>
                      <MenuItem value="darkTheme">Тёмная</MenuItem>
                    </Select>
                  </FormControl>
                </div>
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
}

export default Header;
