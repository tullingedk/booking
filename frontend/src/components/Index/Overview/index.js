import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

import SeatDialog from "./SeatDialog";

// bad practice: should not hard-code

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
    cursor: "pointer",
  },
}));

function Overview() {
  const classes = useStyles();

  function Row(props) {
    return (
      <React.Fragment>
        {Array(parseInt(props.max) - parseInt(props.min) + 1)
          .fill()
          .map((_, idx) => parseInt(props.min) + idx)
          .map(function (id) {
            return (
              <Grid item xs={1}>
                <SeatDialog paper={classes.paper} id={id} />
              </Grid>
            );
          })}
      </React.Fragment>
    );
  }

  return (
    <div className={classes.root}>
      <Grid container spacing={1}>
        <Grid container item xs={8} spacing={1}>
          <Row min={1} max={6} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={7} max={12} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={13} max={18} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={19} max={24} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={25} max={30} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={31} max={36} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={37} max={42} />
        </Grid>
        <Grid container item xs={8} spacing={1}>
          <Row min={43} max={48} />
        </Grid>
      </Grid>
    </div>
  );
}

export default Overview;
