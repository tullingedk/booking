import React, { useEffect, useState } from "react";

import { Container, Button } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function Login() {
  const [loginUrl, setLoginUrl] = useState();

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/auth/login`)
      .then((response) => response.json())
      .then((data) => {
        setLoginUrl(data.response.login_url);
      });
  }, []);

  return (
    <Container maxWidth="sm">
      <Typography variant="h2" gutterBottom align="center">
        Tullinge Datorklubb
      </Typography>
      <Typography variant="body1" gutterBottom align="center">
        Bokningssystem för Tullinge gymnasium datorklubb.
      </Typography>

      <Button variant="contained" color="primary" href={loginUrl}>
        Logga in med Google
      </Button>
    </Container>
  );
}

export default Login;
