import React, { useState } from "react";
import { useDispatch, useSelector } from "react-redux";

// material-ui
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Alert from "@material-ui/lab/Alert";
import TextField from "@material-ui/core/TextField";

// redux
import { fetchBookings } from "../../../redux/bookingActions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function EditDialog(props) {
  const dispatch = useDispatch();

  const [open, setOpen] = useState(false);
  const [error, setError] = useState("");

  const [edit, setEdit] = useState(props.initial_value);

  const bookingReducer = useSelector((state) => state.bookingReducer);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleSubmit = (e) => {
    if (e) {
      e.preventDefault();
    }

    fetch(`${BACKEND_URL}/api/booking/${bookingReducer.dialog_id}`, {
      credentials: "include",
      method: "put",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        [props.variable]: edit,
        seat_type: bookingReducer.dialog_seat_type,
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
      <Button onClick={handleClickOpen} color="secondary">
        Ändra
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">
          Ändra värdet för variabeln {props.variable}
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Använd formuläret nedan för att ändra {props.variable} på plats{" "}
            {bookingReducer.dialog_id}
          </DialogContentText>
          <form onSubmit={handleSubmit} noValidate autoComplete="off">
            <div>
              <TextField
                label="Nytt värde"
                value={edit}
                onChange={(e) => setEdit(e.target.value)}
                helperText="Ange det nya värdet för variabeln."
              />
            </div>{" "}
          </form>
          {error && <Alert severity="error">{error}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Avbryt
          </Button>
          <Button onClick={handleSubmit} color="primary">
            Ändra
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default EditDialog;
