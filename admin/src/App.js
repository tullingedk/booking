import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { Button } from "react-bootstrap";
import Cookies from "js-cookie";
import {
  NotificationContainer,
  NotificationManager
} from "react-notifications";
import "./App.css";

import BookingTable from "./components/BookingTable/index";
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

  const handleLogout = e => {
    if (e) {
      e.preventDefault();
    }

    fetch(`${backend_url}/backend/logout`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        token: props.session_token
      })
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          if (response.status === 502) {
            NotificationManager.error(
              "Kunde inte kommunicera med server",
              "Ett fel uppstod"
            );
            throw new Error("Kunde inte kommunicera med server.");
          } else {
            // other errors are handled by json
            return response.json();
          }
        }
      })
      .then(json => {
        console.log(json.http_code + json.message);

        if (json.http_code === 400) {
          NotificationManager.error(json.message, "Ett fel uppstod");
        } else if (json.http_code === 500) {
          NotificationManager.error(json.message, "Ett fel uppstod");
        } else if (json.http_code === 401) {
          NotificationManager.error(json.message, "Ett fel uppstod");
        } else if (json.http_code === 200) {
          Cookies.remove("session_token");
          window.location.replace("/admin");
        }
      });
  };

  // get data
  const getData = () => {
    fetch(`${backend_url}/backend/bookings`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        token: props.session_token
      })
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          setUpdateFail(true);
          throw new Error("Kunde inte kommunicera med server.");
        }
      })
      .catch(function(error) {
        setUpdateFail(true);
        console.error("Kunde inte kommunicera med backend-server.");
      })
      .then(json => {
        console.log(json);
        setBookings(json.response.bookings);
      });

    fetch(`${backend_url}/backend/bc/bookings`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        token: props.session_token
      })
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          setUpdateFail(true);
          throw new Error("Kunde inte kommunicera med server.");
        }
      })
      .then(json => {
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

        <form onSubmit={handleLogout}>
          <Button style={{ margin: "0.15em" }} type="submit">
            Logga ut
          </Button>
        </form>

        <Row>
          <Column>
            <TableTitle>Vanliga platser</TableTitle>

            <BookingTable
              start_range="0"
              end_range="20"
              columns="2"
              bookings={bookings}
              seat_type={true}
              session_token={props.session_token}
            />

            <BookingTable
              start_range="20"
              end_range="36"
              columns="2"
              bookings={bookings}
              seat_type={true}
              session_token={props.session_token}
            />

            <BookingTable
              start_range="36"
              end_range="48"
              columns="2"
              bookings={bookings}
              seat_type={true}
              session_token={props.session_token}
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
              session_token={props.session_token}
            />
          </ColumnTwo>
        </Row>
      </Container>
      <NotificationContainer />
    </div>
  );
}

export default App;
