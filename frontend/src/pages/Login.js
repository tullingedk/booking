import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";

import { Container, Button, CircularProgress, Grid } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function Login() {
  const meta = useSelector((state) => state.systemMeta);

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
      <Typography variant="h4" gutterBottom align="center">
        Datorklubben Bokningssystem
      </Typography>
      <Typography variant="body1" gutterBottom align="center">
        Denna sida använder en cookie för att hantera inloggningen. Inga
        personuppgifter delas med tredjepart. Efter LAN:et raderas samtliga
        personuppgifter. För frågor, kontakta{" "}
        <Link href="mailto:info@tgdk.se">info@tgdk.se</Link>.
      </Typography>
      <Typography variant="caption" display="block" align="center" gutterBottom>
        © Tullinge Gymnasium Datorklubb, org.nr. 802530-4208
      </Typography>

      <Typography align="center" variant="caption" gutterBottom display="block">
        Kör{" "}
        <Link href="https://github.com/tullingedk/booking">
          tullingedk/booking
        </Link>{" "}
        {meta.version ? meta.version : "unknown"}, commit{" "}
        {meta.hash ? meta.hash : "unknown"} ({meta.hash ? meta.hash : "unknown"}
        )
      </Typography>
      <Typography align="center" variant="caption" gutterBottom display="block">
        Kodat av <Link href="https://vilhelmprytz.se">Vilhelm Prytz</Link>
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
