import React, { useState } from 'react';
import styled from 'styled-components';
import './App.css';

import backend_url from './global_variables';

const Container = styled.div`
    padding: 1em;
    width: 100vmin;
    margin: auto;
    text-align: center;
`

function App(props) {

  // retrieves all bookings using token
  function get_bookings(token) {
    return fetch(`${backend_url}/backend/bookings`, {
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
      return json.response.bookings;
    });
  }

  const bookings = get_bookings(props.session_token);

  return (
    <div className="App">
      <Container>
        <h1>Datorklubben Bokningssystem</h1>
        <p>Kör version {props.info_json.response.version}.</p>
        <p>LAN-datum: {props.info_json.response.event_date}</p>
      </Container>
    </div>
  );
}

export default App;