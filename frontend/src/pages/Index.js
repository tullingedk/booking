import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";

// components for this page
import Nav from "../components/Index/Nav";
import Overview from "../components/Index/Overview";
import AdminDialog from "../components/Index/AdminDialog";
import AdminUserDialog from "../components/Index/AdminUserDialog";
import BookingDialog from "../components/Index/BookingDialog";
import InfoDialog from "../components/Index/InfoDialog";
import SeatDialog from "../components/Index/Booking/SeatDialog";

import ErrorDialog from "../components/ErrorDialog";

// material-ui
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import Link from "@material-ui/core/Link";

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
        <Typography gutterBottom align="center">
          Bokade platser: {bookingReducer.bookings.length}/
          {bookingReducer.num_seats} (alltså{" "}
          {bookingReducer.num_seats - bookingReducer.bookings.length} lediga)
        </Typography>
        <Typography gutterBottom align="center">
          Bokade konsol- och brädspelsplatser:{" "}
          {bookingReducer.console_bookings.length}/
          {bookingReducer.num_console_seats} (alltså{" "}
          {bookingReducer.num_console_seats -
            bookingReducer.console_bookings.length}{" "}
          lediga)
        </Typography>
        <Typography gutterBottom align="center">
          Vid frågor angående bokningen (t.ex. avbokning, platsbyte) eller
          betalningar, kontakta {event.swish_name} via Discord/Vklass.
        </Typography>
        <Grid gutterBottom={true} container spacing={3}>
          {user.is_admin && (
            <>
              <Grid item xs>
                <AdminDialog />
              </Grid>
              <Grid item xs>
                <AdminUserDialog />
              </Grid>
            </>
          )}
          <Grid item xs>
            <BookingDialog
              seat_type="standard"
              title="Boka plats"
              info="En vanlig plats innebär bordsplacering med plats för dator, stol och
              skärm under hela LAN-et. Har du konsol med dig måste du boka
              Datorplats och ha med dig skärm. Läs mer under 'information' knappen."
            />
          </Grid>
          <Grid item xs>
            <BookingDialog
              seat_type="console"
              title="Boka konsol- och brädspelsplats"
              info="En konsol- och brädspelsplats innebär ingen specifik
              plats. Det kommer finnas bord att spela brädspel på och eller
              kort/rollspel. Tillgång till några spelkonsoler som står
              uppställda i biblioteket. Läs mer under 'information' knappen."
            />
          </Grid>
          <Grid item xs>
            <InfoDialog />
          </Grid>
        </Grid>
        {bookingReducer.error && <ErrorDialog message={bookingReducer.error} />}
        <SeatDialog />
        <Overview seat_type="standard" />
        <Typography variant="caption" gutterBottom>
          Kör{" "}
          <Link href="https://github.com/tullingedk/booking">
            tullingedk/booking
          </Link>{" "}
          {meta.version}, commit {meta.hash} ({meta.hashDate})
        </Typography>
        <Typography
          align="center"
          variant="caption"
          gutterBottom
          display="block"
        >
          Kodat av <Link href="https://vilhelmprytz.se">Vilhelm Prytz</Link>
        </Typography>
      </Container>
    </div>
  );
}

export default Index;
