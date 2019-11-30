import React from "react";
import styled from "styled-components";

import SeatModal from "./../SeatModal/index";

const Table = styled.div`
  float: left;
  padding-left: 2em;
  padding-right: 2em;
`;

const Column = styled.div`
  float: left;
  padding: 0.2em;
`;

const SeatText = styled.p`
  padding: 0px;
  padding-top: 0.3em;
  margin: auto;
  font-size: 1.2em;
`;

function BookingColumn(props) {
  const per_column_list = [];
  var seat_counter =
    parseInt(props.start_range) +
    ((parseInt(props.end_range) - parseInt(props.start_range)) /
      parseInt(props.columns)) *
      props.i;
  for (
    var i = 0;
    i <
    (parseInt(props.end_range) - parseInt(props.start_range)) /
      parseInt(props.columns);
    i++
  ) {
    per_column_list.push(i);
  }

  return (
    <Column>
      {per_column_list.map(function(seat_object, x) {
        seat_counter++;
        return (
          <SeatModal
            session_token={props.session_token}
            bookings={props.bookings}
            id={seat_counter}
            seat_type={props.seat_type}
          >
            <SeatText>{seat_counter}</SeatText>
          </SeatModal>
        );
      })}
    </Column>
  );
}

function BookingTable(props) {
  const seats = [];
  const column_list = [];

  for (
    var i = parseInt(props.start_range);
    i <= parseInt(props.end_range);
    i++
  ) {
    seats.push(i);
  }
  for (var y = 0; y < parseInt(props.columns); y++) {
    column_list.push(y);
  }

  return (
    <Table>
      {column_list.map(function(object, i) {
        return (
          <BookingColumn
            session_token={props.session_token}
            start_range={props.start_range}
            end_range={props.end_range}
            columns={props.columns}
            i={i}
            bookings={props.bookings}
            seat_type={props.seat_type}
          />
        );
      })}
    </Table>
  );
}

export default BookingTable;
