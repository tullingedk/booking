import React, { useState, useEffect } from "react";

import md5 from "md5";

// material-ui
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import Avatar from "@material-ui/core/Avatar";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemAvatar from "@material-ui/core/ListItemAvatar";
import ListItemText from "@material-ui/core/ListItemText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Dialog from "@material-ui/core/Dialog";
import Container from "@material-ui/core/Container";
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from "@material-ui/icons/Delete";
import AddIcon from "@material-ui/icons/Add";
import { blue } from "@material-ui/core/colors";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const useStyles = makeStyles({
  avatar: {
    backgroundColor: blue[100],
    color: blue[600],
  },
});

function SimpleDialog(props) {
  const classes = useStyles();
  const { onClose, selectedValue, open } = props;

  const handleClose = () => {
    onClose(selectedValue);
  };

  const addAdmin = (value) => {
    console.log(value);
  };

  const deleteAdmin = (value) => {
    fetch(`${BACKEND_URL}/api/admin/user`, {
      credentials: "include",
      method: "delete",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: value,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
      });
  };

  return (
    <Dialog
      onClose={handleClose}
      aria-labelledby="simple-dialog-title"
      open={open}
    >
      <DialogTitle id="simple-dialog-title">Hantera adminanvändare</DialogTitle>
      <List>
        {props.emails.map((email) => (
          <ListItem button key={email}>
            <ListItemAvatar>
              <Avatar
                className={classes.avatar}
                alt={email}
                src={`https://www.gravatar.com/avatar/${md5(email)}`}
              />
            </ListItemAvatar>
            <ListItemText primary={email} />
            <IconButton onClick={() => deleteAdmin(email)} aria-label="delete">
              <DeleteIcon />
            </IconButton>
          </ListItem>
        ))}

        <ListItem autoFocus button onClick={() => addAdmin("addAccount")}>
          <ListItemAvatar>
            <Avatar>
              <AddIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Lägg till konto" />
        </ListItem>
      </List>
    </Dialog>
  );
}

SimpleDialog.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  selectedValue: PropTypes.string.isRequired,
};

function AdminDialog() {
  const [emails, setEmails] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/admin/user`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          // if 200, all is good
          setEmails(data.response.map((a) => a.email));
        } else {
          setError(`Ett fel uppstod: ${data.message}`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  }, []);

  const [open, setOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState(emails[1]);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = (value) => {
    setOpen(false);
    setSelectedValue(value);
  };

  return (
    <Container maxWidth="sm">
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        Hantera Adminanvändare
      </Button>
      <SimpleDialog
        selectedValue={selectedValue}
        open={open}
        onClose={handleClose}
        emails={emails}
      />
    </Container>
  );
}

export default AdminDialog;
