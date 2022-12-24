import React from "react";
import ReactMarkdown from "react-markdown";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";

class TaskDescription extends React.Component {
  render() {
    return (
      <div>
        <FormControl fullWidth>
          <InputLabel id="task-label">Task</InputLabel>
          <Select labelId="task-label" label="Task">
            <MenuItem value="task1">task1</MenuItem>
            <MenuItem value="task2">task2</MenuItem>
            <MenuItem value="task3">task3</MenuItem>
          </Select>
        </FormControl>
        <ReactMarkdown
          children={`### Hello, world!
        
Here goes the task **description** that uses *markdown* syntax.
- abc
- xyz
- blah blah`}
        />
      </div>
    );
  }
}

export default TaskDescription;
