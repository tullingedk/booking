import React, { useEffect, useState } from "react";

import { Container, Button, CircularProgress, Grid } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import Typography from "@material-ui/core/Typography";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function Login() {
  const [loginUrl, setLoginUrl] = useState();
  const [error, setError] = useState();

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/auth/login`)
      .then((response) => response.json())
      .then((data) => {
        setLoginUrl(data.response.login_url);
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  }, []);

  return (
    <Container maxWidth="sm">
      <Typography variant="h2" gutterBottom align="center">
        Datorklubben Bokningssystem
      </Typography>
      <Typography variant="body1" gutterBottom align="center">
        Bokningssystem för Tullinge gymnasium datorklubb.
      </Typography>

      {loginUrl && (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Grid container justify="center" spacing={1}>
              <Button variant="contained" color="primary" href={loginUrl}>
                Logga in med Google
              </Button>
            </Grid>
          </Grid>
        </Grid>
      )}
      {!loginUrl && !error && (
        <Grid container spacing={2}>
          <Grid item xs={12}>
            <Grid container justify="center" spacing={1}>
              <CircularProgress />
            </Grid>
          </Grid>
        </Grid>
      )}
      {error && <Alert severity="error">{error}</Alert>}
    </Container>
  );
}

export default Login;
