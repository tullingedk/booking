import React from "react";

import { Container } from "@material-ui/core";
import Alert from "@material-ui/lab/Alert";
import Typography from "@material-ui/core/Typography";
import Link from "@material-ui/core/Link";

function Error(props) {
  return (
    <Container maxWidth="sm">
      <Typography variant="h4" gutterBottom align="center">
        Datorklubben Bokningssystem
      </Typography>
      <Alert severity="error">{props.error}</Alert>
      <Typography align="center" variant="caption" gutterBottom display="block">
        Kodat av <Link href="https://vilhelmprytz.se">Vilhelm Prytz</Link>
      </Typography>
    </Container>
  );
}

export default Error;
