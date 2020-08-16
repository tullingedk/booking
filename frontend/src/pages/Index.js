import React, { useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";

// components for this page
import Nav from "../components/Index/Nav";
import Overview from "../components/Index/Overview";
import AdminDialog from "../components/Index/AdminDialog";
import BookingDialog from "../components/Index/BookingDialog";

import ErrorDialog from "../components/ErrorDialog";

// redux
import { fetchBookings } from "../redux/bookingActions";

function Index() {
  // redux
  const dispatch = useDispatch();
  const user = useSelector((state) => state.user);
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
      {user.is_admin && <AdminDialog />}
      <BookingDialog />
      {bookingReducer.error && <ErrorDialog message={bookingReducer.error} />}
      <Overview />
    </div>
  );
}

export default Index;
