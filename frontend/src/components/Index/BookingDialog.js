import React, { useState } from "react";
import { useDispatch } from "react-redux";

// material-ui
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Alert from "@material-ui/lab/Alert";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import Link from "@material-ui/core/Link";

// redux
import { fetchBookings } from "../../redux/bookingActions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function BookingDialog(props) {
  const dispatch = useDispatch();

  const [open, setOpen] = useState(false);
  const [available, setAvailable] = useState([]);
  const [error, setError] = useState("");

  const [seat, setSeat] = useState("");

  const handleClickOpen = () => {
    setOpen(true);
    updateAvailableSeatList();
  };

  const handleClose = () => {
    setOpen(false);
  };

  const updateAvailableSeatList = () => {
    fetch(`${BACKEND_URL}/api/booking/available`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          // if 200, all is good
          if (props.seat_type === "standard") {
            setAvailable(data.response.available_seats.map((a) => a));
          } else if (props.seat_type === "console") {
            setAvailable(data.response.available_console_seats.map((a) => a));
          } else {
            setError(
              `Allvarligt felaktigt meddelande från server: ${data.message} (${data.http_code})`
            );
          }
        } else {
          setError(`Ett fel uppstod: ${data.message} (${data.http_code})`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  };

  const handleSubmit = () => {
    fetch(`${BACKEND_URL}/api/booking/book`, {
      credentials: "include",
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        seat: seat,
        seat_type: props.seat_type,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          dispatch(fetchBookings());
          handleClose();
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
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        {props.title}
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">{props.title}</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Använd formuläret nedan för att boka en plats. Registrera dig som
            medlem på <Link href="https://member.tgdk.se">member.tgdk.se</Link>{" "}
            innan du bokar! {props.info}
          </DialogContentText>
          <Select
            labelId="booking-dialog-select-form"
            id="booking-help-label"
            value={seat}
            onChange={(e) => setSeat(e.target.value)}
          >
            {Array.from(available).map(function (object) {
              return (
                <MenuItem key={object} value={object}>
                  {object}
                </MenuItem>
              );
            })}
          </Select>
          <FormHelperText>Välj en plats ur listan</FormHelperText>
          {error && <Alert severity="error">{error}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Avbryt
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Boka
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default BookingDialog;
