import React from "react";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import InfoIcon from "@mui/icons-material/Info";
import Grid from "@mui/material/Grid";

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
            <Button
              variant="text"
              startIcon={<InfoIcon />}
              href="https://github.com/m-danya/prolog-testing-system"
              target="_blank"
            >
              About
            </Button>
          </Grid>
        </Grid>
      </div>
    );
  }
}

export default Header;
