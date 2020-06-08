import React, { useState } from "react";
import { useSelector } from "react-redux";

// material-ui
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import Typography from "@material-ui/core/Typography";
import IconButton from "@material-ui/core/IconButton";
import Avatar from "@material-ui/core/Avatar";
import MenuItem from "@material-ui/core/MenuItem";
import Menu from "@material-ui/core/Menu";

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
}));

function Nav() {
  const userName = useSelector((state) => state.userName);
  const userClass = useSelector((state) => state.userClass);
  const userAvatar = useSelector((state) => state.userAvatar);
  const meta = useSelector((state) => state.systemMeta);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  const classes = useStyles();
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography variant="h6" className={classes.title}>
          Tullinge Gymnasium Datorklubb - Bokingssystem
        </Typography>
        <Typography variant="caption" className={classes.title}>
          Kör tullingedk/booking {meta.version}, commit {meta.hash}
        </Typography>
        <Typography variant="h6" className={classes.menuButton}>
          {userName} {userClass}
        </Typography>
        <div>
          <IconButton
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
          >
            <Avatar alt={userName} src={userAvatar} />
          </IconButton>
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            keepMounted
            transformOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
            open={open}
            onClose={handleClose}
          >
            <MenuItem
              onClick={() => {
                window.location.replace(`${BACKEND_URL}/api/auth/logout`);
              }}
            >
              Logga ut
            </MenuItem>
          </Menu>
        </div>
      </Toolbar>
    </AppBar>
  );
}

export default Nav;
