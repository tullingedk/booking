import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

import SeatDialog from "./SeatDialog";

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

function isEven(n) {
  return n % 2 === 0;
}

function isOdd(n) {
  return Math.abs(n % 2) === 1;
}

function Overview() {
  const classes = useStyles();

  function Row(props) {
    return (
      <React.Fragment>
        {Array(parseInt(props.max) - parseInt(props.min) + 1)
          .fill()
          .map((_, idx) => parseInt(props.min) + idx)
          .map(function (id) {
            let table_spacing = 0;
            if (isEven(props.min) && isEven(id)) {
              table_spacing = 20;
            }
            if (isOdd(props.min) && isOdd(id)) {
              table_spacing = 20;
            }
            return (
              <Grid
                style={{ paddingLeft: `${table_spacing}px` }}
                key={id}
                item
                xs={2}
              >
                <SeatDialog paper={classes.paper} id={id} />
              </Grid>
            );
          })}
      </React.Fragment>
    );
  }

  // bad practice: should not hard-code
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
          <Row min={37} max={40} />
        </Grid>
      </Grid>
    </div>
  );
}

export default Overview;
