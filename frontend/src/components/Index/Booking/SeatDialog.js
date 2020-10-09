import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// material-ui
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Alert from "@material-ui/lab/Alert";

// booking
import MoveSeatDialog from "./MoveSeatDialog";
import EditDialog from "./EditDialog";

// redux
import { fetchBookings, setBookingDialog } from "../../../redux/bookingActions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function SeatDialog() {
  const bookingReducer = useSelector((state) => state.bookingReducer);
  // const [open, setOpen] = useState(false);

  const user = useSelector((state) => state.user);
  const event = useSelector((state) => state.event);
  const dispatch = useDispatch();

  const booking =
    bookingReducer.dialog_seat_type === "standard"
      ? bookingReducer.bookings.find(
          (seat) => seat.seat === bookingReducer.dialog_id
        )
      : bookingReducer.console_bookings.find(
          (seat) => seat.seat === bookingReducer.dialog_id
        );
  const [error, setError] = useState("");

  const handleClose = () => {
    dispatch(setBookingDialog(false, null, null));
  };

  const changePaymentStatus = (paymentStatus) => {
    fetch(`${BACKEND_URL}/api/booking/${bookingReducer.dialog_id}`, {
      credentials: "include",
      method: "put",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        paid: paymentStatus,
        seat_type: bookingReducer.dialog_seat_type,
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
      <Dialog
        open={bookingReducer.dialog_open}
        onClose={handleClose}
        aria-labelledby="dialog-title"
        aria-describedby="dialog-description"
      >
        <DialogTitle id="dialog-title">
          {bookingReducer.dialog_seat_type === "standard"
            ? "Plats"
            : "Konsol- och brädspelsplats"}{" "}
          {bookingReducer.dialog_id}
        </DialogTitle>
        {booking && bookingReducer.dialog_open && (
          <>
            <DialogContent dividers>
              <Typography gutterBottom>
                Bokad av: {booking.name}
                <EditDialog variable="name" initial_value={booking.name} />
              </Typography>
              <Typography gutterBottom>
                Klass: {booking.school_class}
                <EditDialog
                  variable="school_class"
                  initial_value={booking.school_class}
                />
              </Typography>
              <Typography gutterBottom>
                Bokades: {booking.time_created}
              </Typography>
              <Typography gutterBottom>
                Modifierades senast: {booking.time_updated}
              </Typography>
              <Typography gutterBottom>
                Betald: {booking.paid ? "Ja" : "Nej"}
              </Typography>
              {error && <Alert severity="error">{error}</Alert>}
              {!booking.paid && (
                <>
                  <img
                    alt={`Swish QR-kod för plats ${bookingReducer.dialog_id}`}
                    src={`${BACKEND_URL}/api/booking/swish/${bookingReducer.dialog_seat_type}/${bookingReducer.dialog_id}`}
                    width="100%"
                  />
                  <Typography>
                    Skanna QR-koden ovan med Swishappen. Vid frågor angående
                    bokningen eller betalningar, kontakta {event.swish_name} via
                    Discord.
                  </Typography>
                </>
              )}
            </DialogContent>
            {user.is_admin && (
              <DialogActions>
                <Button
                  onClick={() => changePaymentStatus(true)}
                  color="primary"
                >
                  Markera som betald
                </Button>
                <Button
                  onClick={() => changePaymentStatus(false)}
                  color="secondary"
                >
                  Markera som obetald
                </Button>
                <MoveSeatDialog />
              </DialogActions>
            )}
          </>
        )}
      </Dialog>
    </div>
  );
}

export default SeatDialog;
