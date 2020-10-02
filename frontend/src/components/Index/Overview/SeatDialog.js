import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// material-ui
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import Alert from "@material-ui/lab/Alert";
import Tooltip from "@material-ui/core/Tooltip";

// redux
import { fetchBookings } from "../../../redux/bookingActions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function SeatDialog(props) {
  const [open, setOpen] = useState(false);

  const bookings = useSelector((state) => state.bookingReducer.bookings);
  const console_bookings = useSelector(
    (state) => state.bookingReducer.console_bookings
  );

  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();
  const booking =
    props.seat_type === "standard"
      ? bookings.find((seat) => seat.seat === props.id)
      : console_bookings.find((seat) => seat.seat === props.id);
  const [error, setError] = useState("");

  const handleClickOpen = () => {
    if (booking) {
      setOpen(true);
    }
  };

  const handleClose = () => {
    setOpen(false);
  };

  const changePaymentStatus = (paymentStatus) => {
    fetch(`${BACKEND_URL}/api/booking/${props.id}`, {
      credentials: "include",
      method: "put",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        paid: paymentStatus,
        seat_type: props.seat_type,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          dispatch(fetchBookings());
        } else {
          setError(`Ett fel uppstod: ${data.message} (${data.http_code})`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  };

  return (
    <div>
      <Tooltip
        title={booking ? `${booking.name} ${booking.school_class}` : ""}
        placement="top"
      >
        <Paper
          style={{
            backgroundColor: booking ? (booking.paid ? "red" : "yellow") : "",
          }}
          className={props.paper}
          onClick={handleClickOpen}
          xs={6}
        >
          {props.id}
        </Paper>
      </Tooltip>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
      >
        <DialogTitle id="dialog-title">
          {props.seat_type === "standard"
            ? "Plats"
            : "Konsol- och brädspelsplats"}{" "}
          {props.id}
        </DialogTitle>
        {(booking || open) && (
          <>
            <DialogContent dividers>
              <Typography gutterBottom>Bokad av: {booking.name}</Typography>
              <Typography gutterBottom>
                Klass: {booking.school_class}
              </Typography>
              <Typography gutterBottom>
                Bokades: {booking.time_created}
              </Typography>
              <Typography gutterBottom>
                Betald: {booking.paid ? "Ja" : "Nej"}
              </Typography>
              {error && <Alert severity="error">{error}</Alert>}
              {!booking.paid && (
                <img
                  alt={`Swish QR-kod för plats ${props.id}`}
                  src={`${BACKEND_URL}/api/booking/swish/${props.seat_type}/${props.id}`}
                  width="100%"
                />
              )}
            </DialogContent>
            {user.is_admin && (
              <DialogActions>
                <Button
                  onClick={() => changePaymentStatus(true)}
                  color="primary"
                  autoFocus
                >
                  Markera som betald
                </Button>
                <Button
                  autoFocus
                  onClick={() => changePaymentStatus(false)}
                  color="secondary"
                >
                  Markera som obetald
                </Button>
              </DialogActions>
            )}
          </>
        )}
      </Dialog>
    </div>
  );
}

export default SeatDialog;
