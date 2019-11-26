import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import './App.css';

import BookModal from './components/BookModal/index';
import BookingTable from './components/BookingTable/index';

import backend_url from './global_variables';

const Container = styled.div`
  padding: 1em;
  width: 100vmin;
  margin: auto;
  text-align: center;
`

const Text = styled.p`
  padding: 0px;
  margin: auto;
`

function App(props) {
  const [bookings, setBookings] = useState(0);
  const [bc_bookings, setBcBookings] = useState(0);

  // retrieves all bookings using token
  useEffect(() => {
    fetch(`${backend_url}/backend/bookings`, {
      method: "POST",
      headers: {
          "Accept": 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          token: props.session_token,
      })
    })
    .then((response) => {
      if(response.ok) {
          return response.json();
      } else {
          throw new Error('Kunde inte kommunicera med server.');
      }
    })
    .then((json) => {
      console.log(json)
      setBookings(json.response.bookings);
    });

    fetch(`${backend_url}/backend/bc/bookings`, {
      method: "POST",
      headers: {
          "Accept": 'application/json',
          'Content-Type': 'application/json',
      },
      body: JSON.stringify({
          token: props.session_token,
      })
    })
    .then((response) => {
      if(response.ok) {
          return response.json();
      } else {
          throw new Error('Kunde inte kommunicera med server.');
      }
    })
    .then((json) => {
      console.log(json)
      setBcBookings(json.response.bookings);
    });
  }, [props.session_token]);

  return (
    <div className="App">
      <Container>
        <h1>Datorklubben Bokningssystem</h1>
        <Text>Kör version {props.info_json.response.version}.</Text>
        <Text>LAN-datum: {props.info_json.response.event_date}</Text>
        <Text>{props.info_json.response.int_booked_seats} bokade platser, alltså {props.info_json.response.int_available_seats} lediga platser.</Text>
        <BookModal
          button_text="Boka en vanlig plats"
          modal_title="Boka en vanlig plats"
          modal_desc="Fyll i formuläret nedan för att boka en plats."
          request_url="/book"
          session_token={props.session_token}
        />

        <BookModal 
          button_text="Boka en konsol- och brädsspelsplats"
          modal_title="Boka en konsol- och brädsspelsplats"
          modal_desc="Fyll i formuläret nedan för att boka en plats."
          request_url="/bc/book"
          session_token={props.session_token}
        />

        <BookingTable
          start_range="0"
          end_range="20"
          columns="2"
          bookings={bookings}
        />

        <BookingTable
          start_range="20"
          end_range="40"
          columns="2"
          bookings={bookings}
        />

        <BookingTable
          start_range="40"
          end_range="60"
          columns="2"
          bookings={bookings}
        />

      </Container>
    </div>
  );
}

export default App;