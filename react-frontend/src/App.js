import React from "react";

import axios from "axios";

import Container from "@mui/material/Container";
import CssBaseline from '@mui/material/CssBaseline';
import Grid from "@mui/material/Grid";
import { createTheme, ThemeProvider } from '@mui/material/styles';

import CodeForm from "./CodeForm";
import ExecutionResults from "./ExecutionResults";
import Header from "./Header";
import TaskDescription from "./TaskDescription";
import { lightTheme, darkTheme } from "./Themes.js"

const BACKEND_ADDRESS = process.env.REACT_APP_BACKEND_URL;
const HLP_DEFAULT_CODE = `my_prefix(L, nil);
my_prefix(A.L, A.nil);
my_prefix(A.L1, A.L2) <- my_prefix(L1, L2);`;
const PROLOG_DEFAULT_CODE = `my_prefix(L, []).
my_prefix([A|L], [A|[]]).
my_prefix([A|L1], [A|L2]) :- my_prefix(L1, L2).`;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      task_names: [],
      task_descriptions: [],
      submission_text: HLP_DEFAULT_CODE,
      language: "HLP",
      selected_task_name: "",
      selected_task_description: "",
      is_execution_results_opened: false,
      execution_results_data: [],
      execution_is_loading: false,
      selectedTheme: lightTheme,
    };
    this.sendSubmission = this.sendSubmission.bind(this);
    this.handleSubmissionTextChange = this.handleSubmissionTextChange.bind(this);
    this.handleLanguageChange = this.handleLanguageChange.bind(this);
    this.handleTaskNameChange = this.handleTaskNameChange.bind(this);
    this.getTasksInfo = this.getTasksInfo.bind(this);
    this.handleSubmissionTextClear = this.handleSubmissionTextClear.bind(this);
    this.handleSubmissionTextUpdateFromFile = this.handleSubmissionTextUpdateFromFile.bind(this);
    this.handleCloseResults = this.handleCloseResults.bind(this);
    this.handleThemeChange = this.handleThemeChange.bind(this);
  }

  componentDidMount() {
    this.getTasksInfo();
  }

  handleSubmissionTextChange(event) {
    this.setState({ submission_text: event.target.value });
  }

  handleSubmissionTextClear(_) {
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
    let new_language = event.target.value;
    let new_submission_text = this.state.submission_text;
    if (this.state.submission_text === HLP_DEFAULT_CODE && new_language === "gprolog") {
      new_submission_text = PROLOG_DEFAULT_CODE;
    } else if (this.state.submission_text === PROLOG_DEFAULT_CODE && new_language === "HLP") {
      new_submission_text = HLP_DEFAULT_CODE;
    }
    this.setState({ language: new_language, submission_text: new_submission_text });
  }

  handleThemeChange(_) {
    this.setState((prevState, _) => {
        return { selectedTheme: prevState.selectedTheme === darkTheme ? lightTheme : darkTheme };
    })
  }

  handleTaskNameChange(event) {
    let selected_task_description =
      this.state.task_descriptions[this.state.task_names.indexOf(event.target.value)];
    this.setState({
      selected_task_name: event.target.value,
      selected_task_description: selected_task_description,
    });
  }

  handleCloseResults() {
    this.setState({
      is_execution_results_opened: false,
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
        this.setState({
          execution_results_data: execute_response.data.result,
          is_execution_results_opened: true,
          execution_is_loading: false,
        });
      });
    });
    this.setState({ execution_is_loading: true });
  }

  render() {
    return (
      <ThemeProvider theme={this.state.selectedTheme}>
        <CssBaseline/>
        <Container maxWidth="xl">
          <ExecutionResults
            data={this.state.execution_results_data}
            isOpened={this.state.is_execution_results_opened}
            handleCloseResults={this.handleCloseResults}
          />
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Header
                switchTheme={ this.handleThemeChange }
              />
            </Grid>
            <Grid item xs={12} lg={6}>
              <TaskDescription
                task_names={this.state.task_names}
                selected_task_name={this.state.selected_task_name}
                selected_task_description={this.state.selected_task_description}
                handleTaskNameChange={this.handleTaskNameChange}
              />
            </Grid>
            <Grid item xs={12} lg={6}>
              <CodeForm
                sendSubmission={this.sendSubmission}
                submission_text={this.state.submission_text}
                handleSubmissionTextChange={this.handleSubmissionTextChange}
                language={this.state.language}
                handleLanguageChange={this.handleLanguageChange}
                handleSubmissionTextClear={this.handleSubmissionTextClear}
                handleSubmissionTextUpdateFromFile={this.handleSubmissionTextUpdateFromFile}
                execution_is_loading={this.state.execution_is_loading}
              />
            </Grid>
          </Grid>
        </Container>
      </ThemeProvider>
    );
  }
}

export default App;
