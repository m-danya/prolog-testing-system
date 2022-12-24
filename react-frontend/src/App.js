import React from "react";
import Header from "./Header";
import TaskDescription from "./TaskDescription";
import CodeForm from "./CodeForm";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import axios from "axios";

let BACKEND_ADDRESS = "http://127.0.0.1:3001";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      submission_text: "sample program",
      language: "gprolog",
      task: "task_5_1",
    };
    this.sendSubmission = this.sendSubmission.bind(this);
  }

  sendSubmission() {
    let submissionBlob = new Blob([this.state.submission_text], {
      type: "text/plain",
    });
    let submit_formdata = new FormData();
    submit_formdata.append("submission", submissionBlob, "submission.pl");
    // step 1: submit a file
    axios({
      method: "post",
      url: `${BACKEND_ADDRESS}/submit`,
      data: submit_formdata,
      headers: { "Content-Type": "multipart/form-data" },
    }).then((submit_response) => {
      let submission_id = submit_response.data.submission_id;
      // step 2: run tests execution on it
      axios({
        method: "post",
        url: `${BACKEND_ADDRESS}/execute`,
        data: {
          type: this.state.language,
          task: this.state.task,
          submission_id: submission_id,
        },
        headers: { "Content-Type": "application/json" },
      }).then((execute_response) => {
        alert(JSON.stringify(execute_response));
      });
    });
  }

  render() {
    return (
      <div>
        <Container maxWidth="xl">
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Header />
            </Grid>
            <Grid item xs={6}>
              <TaskDescription />
            </Grid>
            <Grid item xs={6}>
              <CodeForm sendSubmission={this.sendSubmission} />
            </Grid>
          </Grid>
        </Container>
      </div>
    );
  }
}

export default App;
