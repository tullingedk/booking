import React from "react";

import { Container } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import Typography from "@material-ui/core/Typography";

function Error(props) {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom align="center">
        Datorklubben Bokningssystem
      </Typography>
      <Alert severity="error">{props.error}</Alert>
    </Container>
  );
}

export default Error;
