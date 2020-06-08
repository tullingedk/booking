import React from "react";
import { useSelector } from "react-redux";

import { Container, Button, Grid } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";

function Index() {
  const userName = useSelector((state) => state.userName);
  const userClass = useSelector((state) => state.userClass);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  return (
    <Container maxWidth="sm">
      <Typography variant="h2" gutterBottom align="center">
        Tullinge Datorklubb
      </Typography>
      <Typography variant="body1" gutterBottom align="center">
        Inloggad som {userName}, klass {userClass}
      </Typography>
      <Grid container spacing={2}>
        <Grid item xs={12}>
          <Grid container justify="center" spacing={1}>
            <Button
              variant="contained"
              color="primary"
              href={`${BACKEND_URL}/api/auth/logout`}
            >
              Logga ut
            </Button>
          </Grid>
        </Grid>
      </Grid>
    </Container>
  );
}

export default Index;
