import React, { useState, useEffect } from "react";
import styled from "styled-components";
import Konami from "react-konami-code";
import "./App.css";

import BookModal from "./components/BookModal/index";
import BookingTable from "./components/BookingTable/index";
import InfoModal from "./components/InfoModal/index";
import ErrorModal from "./components/ErrorModal/index";

import backend_url from "./global_variables";

const Container = styled.div`
  padding: 1em;
  width: 95%;
  max-width: 950px;
  margin: auto;
  text-align: center;
  @media (max-width: 950px) {
    padding: 0px;
  }
`;

const Text = styled.p`
  padding: 0px;
  margin: auto;
`;

const TableTitle = styled.h4`
  text-align: left;
  padding: 0px;
  margin: auto;
`;

const Row = styled.div`
  width: 100%;

  :after {
    content: "";
    display: table;
    clear: both;
  }
`;

const Column = styled.div`
  float: left;
  width: 63%;
  padding: 0.5em;

  @media (max-width: 950px) {
    width: 100%;
    float: none;
    margin: auto;
  }
`;

const ColumnTwo = styled.div`
  float: left;
  width: 37%;
  padding: 0.5em;
  @media (max-width: 950px) {
    width: 100%;
  }
`;

function App(props) {
  const [bookings, setBookings] = useState(0);
  const [bc_bookings, setBcBookings] = useState(0);

  const [updateFail, setUpdateFail] = useState(false);

  // get data
  const getData = () => {
    fetch(`${backend_url}/backend/bookings`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token: props.session_token,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          setUpdateFail(true);
          throw new Error("Kunde inte kommunicera med server.");
        }
      })
      .catch(function (error) {
        setUpdateFail(true);
        console.error("Kunde inte kommunicera med backend-server.");
      })
      .then((json) => {
        console.log(json);
        setBookings(json.response.bookings);
      });

    fetch(`${backend_url}/backend/bc/bookings`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        token: props.session_token,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          setUpdateFail(true);
          throw new Error("Kunde inte kommunicera med server.");
        }
      })
      .then((json) => {
        console.log(json);
        setBcBookings(json.response.bookings);
      });
  };

  // retrieves all bookings using token
  useEffect(() => {
    getData();
  }, [props.session_token]);

  // update every 5 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      getData();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <ErrorModal show_modal={updateFail} />
      <Container>
        <h1>Datorklubben Bokningssystem</h1>
        <Text>
          Kör version {props.info_json.response.version} (commit{" "}
          <i>{props.info_json.response.commit_hash}</i>).
        </Text>
        <Text>LAN-datum: {props.info_json.response.event_date}</Text>
        <Text>
          <b>Vanliga platser</b>
        </Text>
        <Text>
          {props.info_json.response.int_booked_seats} bokade platser, alltså{" "}
          {props.info_json.response.int_available_seats} lediga platser.
        </Text>
        <br />
        <Text>
          <b>Konsol- och brädspelsplatser</b>
        </Text>
        <Text>
          {props.info_json.response.bc_int_booked_seats} bokade platser, alltså{" "}
          {props.info_json.response.bc_int_available_seats} lediga platser.
        </Text>
        <BookModal
          button_text="Boka en vanlig plats"
          modal_title="Boka en vanlig plats"
          modal_desc="Fyll i formuläret nedan för att boka en plats."
          request_url="/book"
          available_seat_list_url="/available_seat_list"
          session_token={props.session_token}
        />

        <BookModal
          button_text="Boka en konsol- och brädspelsplats"
          modal_title="Boka en konsol- och brädspelsplats"
          modal_desc="Fyll i formuläret nedan för att boka en plats."
          request_url="/bc/book"
          available_seat_list_url="/bc/available_seat_list"
          session_token={props.session_token}
        />

        <InfoModal event_date={props.info_json.response.event_date} />

        <Text>
          <b>OBS!</b> Läs informationen ovan innan du bokar en plats!
        </Text>

        <Row>
          <Column>
            <TableTitle>Vanliga platser</TableTitle>

            <BookingTable
              start_range="0"
              end_range="20"
              columns="2"
              bookings={bookings}
              seat_type={true}
            />

            <BookingTable
              start_range="20"
              end_range="36"
              columns="2"
              bookings={bookings}
              seat_type={true}
            />

            <BookingTable
              start_range="36"
              end_range="48"
              columns="2"
              bookings={bookings}
              seat_type={true}
            />
          </Column>
          <ColumnTwo>
            <TableTitle>Konsol- och brädspelsplatser</TableTitle>

            <BookingTable
              start_range="0"
              end_range="10"
              columns="1"
              bookings={bc_bookings}
              seat_type={false}
            />
          </ColumnTwo>
        </Row>
      </Container>
      <Konami
        action={() => {
          window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
        }}
      />
    </div>
  );
}

export default App;
