import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";

// components for this page
import Nav from "../components/Index/Nav";
import Overview from "../components/Index/Overview";
import AdminDialog from "../components/Index/AdminDialog";
import BookingDialog from "../components/Index/BookingDialog";
import InfoDialog from "../components/Index/InfoDialog";
import SeatDialog from "../components/Index/SeatDialog";

import ErrorDialog from "../components/ErrorDialog";

// material-ui
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";

// redux
import { fetchBookings } from "../redux/bookingActions";

function Index() {
  // redux
  const dispatch = useDispatch();
  const user = useSelector((state) => state.user);
  const meta = useSelector((state) => state.systemMeta);
  const event = useSelector((state) => state.event);
  const bookingReducer = useSelector((state) => state.bookingReducer);

  useEffect(() => {
    const interval = setInterval(() => {
      dispatch(fetchBookings());
    }, 5000);
    return () => clearInterval(interval);
  }, [dispatch]);

  return (
    <div>
      <Nav />
      <Container align="center" maxWidth="md">
        <Typography gutterBottom align="center">
          LAN-datum: {event.event_date}
        </Typography>
        <Grid gutterBottom={true} container spacing={3}>
          {user.is_admin && (
            <Grid item xs>
              <AdminDialog />
            </Grid>
          )}
          <Grid item xs>
            <BookingDialog seat_type="standard" title="Boka plats" />
          </Grid>
          <Grid item xs>
            <BookingDialog
              seat_type="console"
              title="Boka konsol- och brädspelsplats"
            />
          </Grid>
          <Grid item xs>
            <InfoDialog />
          </Grid>
        </Grid>
        {bookingReducer.error && <ErrorDialog message={bookingReducer.error} />}
        <SeatDialog />
        <Overview seat_type="standard" />
        <Typography variant="caption">
          Kör tullingedk/booking {meta.version}, commit {meta.hash}
        </Typography>
      </Container>
    </div>
  );
}

export default Index;
