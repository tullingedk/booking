import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// material-ui
import { withStyles } from "@material-ui/core/styles";
import Dialog from "@material-ui/core/Dialog";
import MuiDialogTitle from "@material-ui/core/DialogTitle";
import MuiDialogContent from "@material-ui/core/DialogContent";
import MuiDialogActions from "@material-ui/core/DialogActions";
import IconButton from "@material-ui/core/IconButton";
import CloseIcon from "@material-ui/icons/Close";
import Typography from "@material-ui/core/Typography";
import Button from "@material-ui/core/Button";
import Paper from "@material-ui/core/Paper";
import Alert from "@material-ui/lab/Alert";

// redux
import { fetchBookings } from "../../../redux/bookingActions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const styles = (theme) => ({
  root: {
    margin: 0,
    padding: theme.spacing(2),
  },
  closeButton: {
    position: "absolute",
    right: theme.spacing(1),
    top: theme.spacing(1),
    color: theme.palette.grey[500],
  },
});

const DialogTitle = withStyles(styles)((props) => {
  const { children, classes, onClose, ...other } = props;
  return (
    <MuiDialogTitle disableTypography className={classes.root} {...other}>
      <Typography variant="h6">{children}</Typography>
      {onClose ? (
        <IconButton
          aria-label="close"
          className={classes.closeButton}
          onClick={onClose}
        >
          <CloseIcon />
        </IconButton>
      ) : null}
    </MuiDialogTitle>
  );
});

const DialogContent = withStyles((theme) => ({
  root: {
    padding: theme.spacing(2),
  },
}))(MuiDialogContent);

const DialogActions = withStyles((theme) => ({
  root: {
    margin: 0,
    padding: theme.spacing(1),
  },
}))(MuiDialogActions);

function SeatDialog(props) {
  const bookings = useSelector((state) => state.bookingReducer.bookings);
  const user = useSelector((state) => state.user);
  const dispatch = useDispatch();

  const [open, setOpen] = useState(false);
  const [color, setColor] = useState("");
  const [booking, setBooking] = useState("");
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

  useEffect(() => {
    const search = bookings.find((seat) => seat.seat === props.id);
    if (search) {
      setBooking(search);
      if (search.paid) {
        setColor("red");
      } else {
        setColor("yellow");
      }
    }
  }, [bookings, props.id]);

  return (
    <div>
      <Paper
        style={{ backgroundColor: color }}
        className={props.paper}
        onClick={handleClickOpen}
      >
        {props.id}
      </Paper>
      <Dialog
        onClose={handleClose}
        aria-labelledby="customized-dialog-title"
        open={open}
      >
        <DialogTitle id="customized-dialog-title" onClose={handleClose}>
          Plats {props.id}
        </DialogTitle>
        <DialogContent dividers>
          <Typography gutterBottom>Bokad av: {booking.name}</Typography>
          <Typography gutterBottom>Klass: {booking.school_class}</Typography>
          <Typography gutterBottom>Bokades: {booking.time_created}</Typography>
          <Typography gutterBottom>
            Betald: {booking.paid ? "Ja" : "Nej"}
          </Typography>
          {error && <Alert severity="error">{error}</Alert>}
          {!booking.paid && (
            <img
              alt={`Swish QR-kod för plats ${props.id}`}
              src={`${BACKEND_URL}/api/booking/swish/${props.id}`}
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
      </Dialog>
    </div>
  );
}

export default SeatDialog;
