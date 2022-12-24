import React from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";

import ClearIcon from "@mui/icons-material/Clear";
import SendIcon from "@mui/icons-material/Send";
import FileUploadIcon from "@mui/icons-material/FileUpload";

import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";

class CodeForm extends React.Component {
  render() {
    return (
      <div>
        <Grid
          container
          spacing={2}
          alignItems="center"
          justifyContent="space-between"
          paddingBottom="20px"
        >
          <Grid item>
            <div style={{ width: "150px", maxWidth: "150px" }}>
              <FormControl fullWidth>
                <InputLabel id="programming-language-label">
                  Language
                </InputLabel>
                <Select
                  labelId="programming-language-label"
                  label="Language"
                  defaultValue="gprolog"
                  width="200px"
                >
                  <MenuItem value="gprolog">Prolog</MenuItem>
                  <MenuItem value="HLP">HLP</MenuItem>
                </Select>
              </FormControl>
            </div>
          </Grid>
          <Grid item xs style={{ textAlign: "right" }}>
            <Stack direction="row" spacing={2} justifyContent="flex-end">
              <Button variant="outlined" startIcon={<FileUploadIcon />}>
                Load from file
              </Button>
              <Button variant="outlined" startIcon={<ClearIcon />}>
                Clear
              </Button>
              <Button
                variant="contained"
                endIcon={<SendIcon />}
                onClick={this.props.sendSubmission}
              >
                Run on tests
              </Button>
            </Stack>
          </Grid>
        </Grid>

        <TextField
          label="Your code"
          // error
          multiline
          minRows="15"
          fullWidth
          margin="dense"
          variant="outlined"
          inputProps={{
            style: {
              fontFamily: '"Lucida Console", Courier, monospace',
            },
          }}
          defaultValue={`my_prefix(L, []).
my_prefix([A|L], [A|[]]).
my_prefix([A|L1], [A|L2]) :- my_prefix(L1, L2).`}
        />
      </div>
    );
  }
}

export default CodeForm;
