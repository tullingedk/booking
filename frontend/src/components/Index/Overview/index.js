import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Grid from "@material-ui/core/Grid";

// redux
import { useSelector, useDispatch } from "react-redux";
import { setBookingDialog } from "../../../redux/bookingActions";

// material-ui
import { Typography } from "@material-ui/core";
import Paper from "@material-ui/core/Paper";
import Tooltip from "@material-ui/core/Tooltip";

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

function Overview(props) {
  const classes = useStyles();

  const bookings = useSelector((state) => state.bookingReducer.bookings);
  const console_bookings = useSelector(
    (state) => state.bookingReducer.console_bookings
  );

  const dispatch = useDispatch();

  function Row(props) {
    return (
      <>
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
            const booking =
              props.seat_type === "standard"
                ? bookings.find((seat) => seat.seat === id)
                : console_bookings.find((seat) => seat.seat === id);
            return (
              <Grid
                style={{ paddingLeft: `${table_spacing}px` }}
                key={id}
                item
                xs={2}
              >
                <Tooltip
                  title={
                    booking ? `${booking.name} ${booking.school_class}` : ""
                  }
                  placement="top"
                >
                  <Paper
                    style={{
                      backgroundColor: booking
                        ? booking.paid
                          ? "red"
                          : "yellow"
                        : "",
                    }}
                    className={classes.paper}
                    onClick={() =>
                      dispatch(setBookingDialog(true, id, props.seat_type))
                    }
                    xs={6}
                  >
                    {id}
                  </Paper>
                </Tooltip>
              </Grid>
            );
          })}
      </>
    );
  }

  const row_xs = 12;

  // bad practice: should not hard-code
  return (
    <div className={classes.root}>
      <Typography>
        Platser för deltagare med egen dator/konsol, bordsplacering
      </Typography>
      <Grid container spacing={1}>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={1} max={6} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={7} max={12} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={13} max={18} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={19} max={24} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={25} max={30} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={31} max={36} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={37} max={42} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={43} max={48} seat_type={"standard"} />
        </Grid>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={49} max={55} seat_type={"standard"} />
        </Grid>
      </Grid>
      <Typography>Platser utan bordsplacering</Typography>
      <Grid container>
        <Grid container item xs={row_xs} spacing={1}>
          <Row min={1} max={20} seat_type={"console"} />
        </Grid>
      </Grid>
    </div>
  );
}

export default Overview;
