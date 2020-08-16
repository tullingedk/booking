import React from "react";

// material-ui
import Dialog from "@material-ui/core/Dialog";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import { Alert, AlertTitle } from "@material-ui/lab";
import { Typography } from "@material-ui/core";

function ErrorDialog(props) {
  return (
    <div>
      <Dialog
        open={true}
        aria-labelledby="alert-dialog-title"
        aria-describedby="alert-dialog-description"
      >
        <DialogTitle id="alert-dialog-title">Ett fel uppstod</DialogTitle>
        <DialogContent>
          <DialogContentText id="alert-dialog-description">
            <Alert severity="error">
              <AlertTitle>Ett fel uppstod</AlertTitle>
              {props.message}
            </Alert>
            <Typography>
              Din webbläsare har tappat anslutningen till servern. Ladda om
              sidan för att försöka igen.
            </Typography>
          </DialogContentText>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default ErrorDialog;
