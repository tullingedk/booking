import React from "react";
import { useSelector } from "react-redux";

// material-ui
import Container from "@material-ui/core/Container";

function Table() {
  const bookings = useSelector((state) => state.bookingReducer.bookings);

  return (
    <Container maxWidth="sm">
      {Array.from(bookings).map(function (booking) {
        return (
          <p key={booking.seat} value={booking.seat}>
            {booking.seat} {booking.name}
          </p>
        );
      })}
    </Container>
  );
}

export default Table;
