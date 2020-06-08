import React from "react";

import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";
import Grid from "@material-ui/core/Grid";
import Paper from "@material-ui/core/Paper";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    height: 40,
    width: 40,
  },
}));

function Table() {
  const classes = useStyles();

  function Row(props) {
    return (
      <Grid item className={classes.root} xs={3}>
        <Grid item xs={1}>
          <Grid container justify="center" xs={6}>
            {Array(props.end - props.start + 1)
              .fill()
              .map((_, idx) => props.start + idx)
              .map((value) => (
                <Grid key={value} item>
                  <Paper className={classes.paper}>
                    <Typography align="center" variant="body2" gutterBottom>
                      {value}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
          </Grid>
        </Grid>
      </Grid>
    );
  }

  return (
    <Container maxWidth="sm">
      <Grid container spacing={3}>
        <Row length={16} start={1} end={16} />
        <Row length={16} start={17} end={32} />
        <Row length={16} start={33} end={48} />
      </Grid>
    </Container>
  );
}

export default Table;
