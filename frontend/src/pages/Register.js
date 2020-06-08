import React, { useState } from "react";
import { useDispatch } from "react-redux";

import { Container, TextField, Button, Icon, Grid } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import Typography from "@material-ui/core/Typography";

// redux
import { setAuthenticated } from "./../redux/actions";
import { setRegistered } from "./../redux/actions";
import { setUserEmail } from "./../redux/actions";
import { setUserName } from "./../redux/actions";
import { setUserClass } from "./../redux/actions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function Register() {
  // redux
  const dispatch = useDispatch();

  // form variables
  const [password, setPassword] = useState("");
  const [schoolClass, setSchoolClass] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    if (e) {
      e.preventDefault();
    }

    fetch(`${BACKEND_URL}/api/auth/register`, {
      credentials: "include",
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        password: password,
        school_class: schoolClass,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.http_code === 200) {
          // if 200, all is good
          dispatch(setAuthenticated(true));
          dispatch(setRegistered(true));

          // set user info
          dispatch(setUserEmail(data.response.email));
          dispatch(setUserName(data.response.name));
          dispatch(setUserClass(data.response.school_class));
        } else {
          setError(`${data.message} (${data.http_code})`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  };

  return (
    <Container maxWidth="sm">
      <Typography variant="h2" gutterBottom align="center">
        Tullinge Datorklubb
      </Typography>
      <Typography variant="body1" gutterBottom align="center">
        Du är inloggad men inte registrerad.
      </Typography>

      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Grid container justify="center" spacing={1}>
            <Button
              justify="center"
              variant="contained"
              color="primary"
              href={`${BACKEND_URL}/api/auth/logout`}
            >
              Logga ut
            </Button>
          </Grid>
        </Grid>
      </Grid>

      <Container maxWidth="xs">
        <form onSubmit={handleSubmit} noValidate autoComplete="off">
          <div>
            <TextField
              label="Lösenord"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              helperText="Ange registreringslösenordet från datorklubbens styrelse."
            />
          </div>
          <div>
            <TextField
              label="Klass"
              value={schoolClass}
              onChange={(e) => setSchoolClass(e.target.value)}
              helperText="Ange namnet på din klass"
            />
          </div>
          <br />

          <Button
            variant="contained"
            color="primary"
            endIcon={<Icon>send</Icon>}
            type="submit"
          >
            Registrera
          </Button>
        </form>
      </Container>
      {error && <Alert severity="error">{error}</Alert>}
    </Container>
  );
}

export default Register;
