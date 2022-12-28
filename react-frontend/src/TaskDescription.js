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
          <InputLabel id="task-label">Задача</InputLabel>
          <Select
            labelId="task-label"
            label="Задача"
            value={this.props.selected_task_name}
            onChange={this.props.handleTaskNameChange}
          >
            {this.props.task_names.map((task_name) => (
              <MenuItem value={task_name} key={task_name}>
                {task_name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <ReactMarkdown children={this.props.selected_task_description} />
      </div>
    );
  }
}

export default TaskDescription;
