import React from "react";
import LoadingButton from "@mui/lab/LoadingButton";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";

import ClearIcon from "@mui/icons-material/Clear";
import SendIcon from "@mui/icons-material/Send";
import FileUploadIcon from "@mui/icons-material/FileUpload";

import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Grid from "@mui/material/Grid";
import Stack from "@mui/material/Stack";
import CircularProgress from "@mui/material/CircularProgress";

import "./style.css";

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
                <InputLabel id="programming-language-label">Язык</InputLabel>
                <Select
                  labelId="programming-language-label"
                  label="Язык"
                  width="200px"
                  value={this.props.language}
                  onChange={this.props.handleLanguageChange}
                >
                  <MenuItem value="HLP">ХЛП</MenuItem>
                  <MenuItem value="gprolog">Prolog</MenuItem>
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
                  Из файла
                </Button>
              </label>
              <Button
                variant="outlined"
                startIcon={<ClearIcon />}
                onClick={this.props.handleSubmissionTextClear}
              >
                Очистить
              </Button>
              <LoadingButton
                variant="contained"
                endIcon={<SendIcon />}
                onClick={this.props.sendSubmission}
                loading={this.props.execution_is_loading}
                loadingIndicator={<CircularProgress color="primary" size={18} />}
              >
                Протестировать
              </LoadingButton>
            </Stack>
          </Grid>
        </Grid>

        <TextField
          label="Ваш код"
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
