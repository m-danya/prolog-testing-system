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
      task_names: [],
      task_descriptions: [],
      submission_text: `my_prefix(L, []).
my_prefix([A|L], [A|[]]).
my_prefix([A|L1], [A|L2]) :- my_prefix(L1, L2).`,
      language: "gprolog",
      selected_task_name: "",
      selected_task_description: "",
    };
    this.sendSubmission = this.sendSubmission.bind(this);
    this.handleSubmissionTextChange = this.handleSubmissionTextChange.bind(this);
    this.handleLanguageChange = this.handleLanguageChange.bind(this);
    this.handleTaskNameChange = this.handleTaskNameChange.bind(this);
    this.getTasksInfo = this.getTasksInfo.bind(this);
    this.handleSubmissionTextClear = this.handleSubmissionTextClear.bind(this);
    this.handleSubmissionTextUpdateFromFile = this.handleSubmissionTextUpdateFromFile.bind(this);
  }

  componentDidMount() {
    this.getTasksInfo();
  }

  handleSubmissionTextChange(event) {
    this.setState({ submission_text: event.target.value });
  }

  handleSubmissionTextClear(event) {
    this.setState({ submission_text: "" });
  }

  handleSubmissionTextUpdateFromFile(event) {
    event.preventDefault();
    const reader = new FileReader();
    reader.onload = async (event) => {
      this.setState({
        submission_text: event.target.result,
      });
    };
    reader.readAsText(event.target.files[0]);
  }

  handleLanguageChange(event) {
    this.setState({ language: event.target.value });
  }

  handleTaskNameChange(event) {
    let selected_task_description =
      this.state.task_descriptions[this.state.task_names.indexOf(event.target.value)];
    this.setState({
      selected_task_name: event.target.value,
      selected_task_description: selected_task_description,
    });
  }

  getTasksInfo() {
    axios({
      method: "get",
      url: `${BACKEND_ADDRESS}/tasks_info`,
    }).then((response) => {
      this.setState(
        {
          task_names: response.data.task_names,
          task_descriptions: response.data.task_descriptions,
        },
        () => {
          // select first available task by default
          this.handleTaskNameChange({ target: { value: this.state.task_names[0] } });
        }
      );
    });
  }

  sendSubmission() {
    let submissionBlob = new Blob([this.state.submission_text], {
      type: "text/plain",
    });
    let submit_formdata = new FormData();
    submit_formdata.append("submission", submissionBlob, "submission.txt");
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
          task: this.state.selected_task_name,
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
              <TaskDescription
                task_names={this.state.task_names}
                selected_task_name={this.state.selected_task_name}
                selected_task_description={this.state.selected_task_description}
                handleTaskNameChange={this.handleTaskNameChange}
              />
            </Grid>
            <Grid item xs={6}>
              <CodeForm
                sendSubmission={this.sendSubmission}
                submission_text={this.state.submission_text}
                handleSubmissionTextChange={this.handleSubmissionTextChange}
                language={this.state.language}
                handleLanguageChange={this.handleLanguageChange}
                handleSubmissionTextClear={this.handleSubmissionTextClear}
                handleSubmissionTextUpdateFromFile={this.handleSubmissionTextUpdateFromFile}
              />
            </Grid>
          </Grid>
        </Container>
      </div>
    );
  }
}

export default App;
