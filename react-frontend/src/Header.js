import React from "react";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

class Header extends React.Component {
  render() {
    return (
      <div>
        <Typography variant="h3" style={{ margin: "30px 0" }}>
          Prolog testing system
        </Typography>
      </div>
    );
  }
}

export default Header;
