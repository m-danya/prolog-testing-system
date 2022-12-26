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
                <InputLabel id="programming-language-label">Language</InputLabel>
                <Select
                  labelId="programming-language-label"
                  label="Language"
                  defaultValue="gprolog"
                  width="200px"
                  value={this.props.language}
                  onChange={this.props.handleLanguageChange}
                >
                  <MenuItem value="gprolog">Prolog</MenuItem>
                  <MenuItem value="HLP">HLP</MenuItem>
                </Select>
              </FormControl>
            </div>
          </Grid>
          <Grid item xs style={{ textAlign: "right" }}>
            <Stack direction="row" spacing={2} justifyContent="flex-end">
              <input
                accept=".pl, .hlp, .txt"
                style={{ display: "none" }}
                id="raised-button-file"
                type="file"
                onChange={this.props.handleSubmissionTextUpdateFromFile}
              />
              <label htmlFor="raised-button-file">
                <Button variant="outlined" component="span" startIcon={<FileUploadIcon />}>
                  Load from file
                </Button>
              </label>
              <Button
                variant="outlined"
                startIcon={<ClearIcon />}
                onClick={this.props.handleSubmissionTextClear}
              >
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
          value={this.props.submission_text}
          onChange={this.props.handleSubmissionTextChange}
        />
      </div>
    );
  }
}

export default CodeForm;
