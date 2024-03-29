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
import IconButton from "@material-ui/core/IconButton";
import DeleteIcon from "@material-ui/icons/Delete";
import AddIcon from "@material-ui/icons/Add";
import Alert from "@material-ui/lab/Alert";

import TextField from "@material-ui/core/TextField";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";

import { blue } from "@material-ui/core/colors";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const useStyles = makeStyles({
  avatar: {
    backgroundColor: blue[100],
    color: blue[600],
  },
});

function UserList(props) {
  const [createAdminDialogOpen, setCreateAdminDialogOpen] = useState(false);

  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  const classes = useStyles();
  const { onClose, selectedValue, open } = props;

  const updateAdmins = () => {
    fetch(`${BACKEND_URL}/api/admin/user`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          // if 200, all is good
          setUsers(data.response.map((a) => a));
        } else {
          setError(`Ett fel uppstod: ${data.message} (${data.http_code})`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  };

  useEffect(() => {
    updateAdmins();
  }, []);

  const handleClose = () => {
    onClose(selectedValue);
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
        if (data.http_code === 200) {
          updateAdmins();
        } else {
          setError(`Ett fel uppstod: ${data.message} (${data.http_code})`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  };

  return (
    <Dialog
      onClose={handleClose}
      aria-labelledby="simple-dialog-title"
      open={open}
    >
      <DialogTitle id="simple-dialog-title">Hantera användare</DialogTitle>
      <List>
        {users.map((user) => (
          <ListItem button key={user.email}>
            <ListItemAvatar>
              <Avatar
                className={classes.avatar}
                alt={user.email}
                src={
                  user.google_picture_url
                    ? user.google_picture_url
                    : `https://www.gravatar.com/avatar/${md5(user.email)}`
                }
              />
            </ListItemAvatar>
            <ListItemText primary={`${user.email}, ${user.school_class}`} />
            <IconButton
              onClick={() => deleteAdmin(user.email)}
              aria-label="delete"
            >
              <DeleteIcon />
            </IconButton>
          </ListItem>
        ))}

        <ListItem
          autoFocus
          button
          onClick={() => setCreateAdminDialogOpen(true)}
        >
          <ListItemAvatar>
            <Avatar>
              <AddIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText primary="Lägg till konto" />
        </ListItem>
        {error && <Alert severity="error">{error}</Alert>}
        <CreateUser
          open={createAdminDialogOpen}
          onClose={() => {
            updateAdmins();
            setCreateAdminDialogOpen(false);
          }}
        />
      </List>
    </Dialog>
  );
}

UserList.propTypes = {
  onClose: PropTypes.func.isRequired,
  open: PropTypes.bool.isRequired,
  selectedValue: PropTypes.string.isRequired,
};

function CreateUser(props) {
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [schoolClass, setSchoolClass] = useState("");

  const submit = () => {
    fetch(`${BACKEND_URL}/api/admin/user`, {
      credentials: "include",
      method: "post",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: email,
        school_class: schoolClass,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          setEmail("");
          props.onClose();
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
        open={props.open}
        onClose={props.onClose}
        aria-labelledby="form-dialog-title"
      >
        <DialogTitle id="form-dialog-title">Lägg till användare</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Ange e-postadressen på det Googlekonto du vill lägga till som
            användare.
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="E-post"
            type="email"
            fullWidth
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
            }}
          />
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Skolklass"
            type="text"
            fullWidth
            value={schoolClass}
            onChange={(e) => {
              setSchoolClass(e.target.value);
            }}
          />
          {error && <Alert severity="error">{error}</Alert>}
        </DialogContent>
        <DialogActions>
          <Button onClick={props.onClose} color="primary">
            Avbryt
          </Button>
          <Button onClick={submit} color="primary">
            Skapa
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

function AdminUserDialog() {
  const [open, setOpen] = useState(false);
  const [selectedValue, setSelectedValue] = useState("");

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = (value) => {
    setOpen(false);
    setSelectedValue(value);
  };

  return (
    <>
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        Hantera användare
      </Button>
      <UserList
        selectedValue={selectedValue}
        open={open}
        onClose={handleClose}
      />
    </>
  );
}

export default AdminUserDialog;
