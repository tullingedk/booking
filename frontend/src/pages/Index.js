import React from "react";
import { useSelector } from "react-redux";

// components for this page
import Nav from "../components/Index/Nav";
import Overview from "../components/Index/Overview";
import AdminDialog from "../components/Index/AdminDialog";
import BookingDialog from "../components/Index/BookingDialog";
import InfoDialog from "../components/Index/InfoDialog";

import ErrorDialog from "../components/ErrorDialog";

// material-ui
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";

// redux
// import { fetchBookings } from "../redux/bookingActions";

function Index() {
  // redux
  // const dispatch = useDispatch();
  const user = useSelector((state) => state.user);
  const meta = useSelector((state) => state.systemMeta);
  const bookingReducer = useSelector((state) => state.bookingReducer);

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     dispatch(fetchBookings());
  //   }, 2000);
  //   return () => clearInterval(interval);
  // }, [dispatch]);

  return (
    <div>
      <Nav />
      <Container maxWidth="md">
        {user.is_admin && <AdminDialog />}
        <BookingDialog />
        <InfoDialog />
        {bookingReducer.error && <ErrorDialog message={bookingReducer.error} />}
        <Overview />
        <Typography variant="caption">
          Kör tullingedk/booking {meta.version}, commit {meta.hash}
        </Typography>
      </Container>
    </div>
  );
}

export default Index;
