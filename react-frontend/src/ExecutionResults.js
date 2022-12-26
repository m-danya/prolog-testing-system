import React from "react";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";

class ExecutionResults extends React.Component {
  mapCode(lst) {
    return lst.map((line) => (
      <span
        style={{
          fontFamily: '"Lucida Console", Courier, monospace',
        }}
      >
        {line}
        <br />
      </span>
    ));
  }

  splitAndMapCode(str) {
    return this.mapCode(str.split("\n"));
  }

  render() {
    return (
      <Dialog
        onClose={this.props.handleCloseResults}
        aria-labelledby="dialog-title"
        open={this.props.isOpened}
        fullWidth={true}
        maxWidth="lg"
      >
        <DialogTitle id="dialog-title" onClose={this.props.handleCloseResults}>
          Your program has passed {this.props.data.filter((test) => test.result === "OK").length}/
          {this.props.data.length} tests
        </DialogTitle>
        <DialogContent>
          {this.props.data.length && this.props.data[0].test_consult_text != "—" && (
            <div>
              <Typography variant="subtitle1" gutterBottom>
                This set of tests has following predefined predicates:
              </Typography>
              {this.splitAndMapCode(this.props.data[0].test_consult_text)}
            </div>
          )}
          <Table aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>#</TableCell>
                <TableCell>Result</TableCell>
                <TableCell>Test text</TableCell>
                <TableCell>Program output</TableCell>
                <TableCell>Correct output</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {this.props.data.map((row) => (
                <TableRow key={row.test_number}>
                  <TableCell>{row.test_number}</TableCell>
                  <TableCell
                    style={{
                      color: row.result === "OK" ? "darkgreen" : "darkred",
                      fontWeight: "bold",
                    }}
                  >
                    {row.result}
                  </TableCell>
                  <TableCell>{this.splitAndMapCode(row.test_text)}</TableCell>
                  <TableCell>{this.mapCode(row.output_lines)}</TableCell>
                  <TableCell>{this.mapCode(row.correct_lines)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </DialogContent>
        <DialogActions>
          <Button onClick={this.props.handleCloseResults} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>
    );
  }
}

export default ExecutionResults;
