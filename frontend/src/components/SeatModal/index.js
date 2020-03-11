import React, { useState, useEffect } from "react";
import { Modal, Button, Tooltip, OverlayTrigger } from "react-bootstrap";
import styled from "styled-components";

import backend_url from "./../../global_variables";

const Container = styled.div`
  background-color: white;
`;

const Seat = styled.div`
  border-style: solid;
  margin: auto;
  width: 3em;
  height: 3em;
`;

const Text = styled.p`
  margin: auto;
  padding: 0px;
`;

function SeatModal(props) {
  const [show, setShow] = useState(false);
  const [blockShow, setBlockShow] = useState(true);
  const [cursor, setCursor] = useState("");
  const [showSwish, setShowSwish] = useState(false);
  const handleClose = () => setShow(false);
  const handleShow = () => {
    if (blockShow === false) {
      setShow(true);
    }
  };

  const [seatType, setSeatType] = useState(false);
  const [seatColor, setSeatColor] = useState("white");
  const [name, setName] = useState("");
  const [schoolClass, setSchoolClass] = useState("");
  const [date, setDate] = useState("");
  const [bookingStatus, setBookingStatus] = useState("");

  useEffect(() => {
    var booking = Array.from(props.bookings).filter(obj => {
      return obj.id === props.id;
    });

    if (booking.length !== 0) {
      booking = booking[0];
    }

    if (parseInt(booking.status) === 1) {
      setSeatColor("yellow");
      setBlockShow(false);
      setCursor("pointer");
      setBookingStatus("Obetald");
      setShowSwish(true);
    } else if (parseInt(booking.status) === 0) {
      setSeatColor("red");
      setBlockShow(false);
      setCursor("pointer");
      setBookingStatus("Betald");
      setShowSwish(false);
    }

    setName(booking.name);
    setSchoolClass(booking.school_class);
    setDate(booking.date);
  }, [props.bookings, props.id]);

  useEffect(() => {
    if (props.seat_type) {
      setSeatType(true);
    }
  }, [props.seat_type]);

  return (
    <OverlayTrigger
      placement="top"
      delay={{ show: 250, hide: 400 }}
      overlay={
        <Tooltip style={{ display: show ? "none" : "block" }} id={props.id}>
          {name} {schoolClass}
        </Tooltip>
      }
    >
      <Container style={{ backgroundColor: seatColor, cursor: cursor }}>
        <Seat onClick={handleShow}>{props.children}</Seat>

        <Modal show={show} onHide={handleClose}>
          <Modal.Header closeButton>
            <Modal.Title>
              {seatType ? "Plats" : "Konsol- och brädspelssplats"} {props.id}
            </Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div>
              <Text>Namn: {name}</Text>
              <Text>Klass: {schoolClass}</Text>
              <Text>Bokades: {date}</Text>
              <Text>Status: {bookingStatus}</Text>

              <div
                style={{ display: showSwish ? "block" : "none" }}
                className="swish_qr"
              >
                <img
                  width="80%"
                  height="80%"
                  src={`${backend_url}/backend${seatType ? "/" : "/bc/"}swish/${
                    props.id
                  }`}
                  alt={props.id}
                />
                <p>
                  Denna bokning är markerad som ej betald. Du kan skanna koden
                  ovan i Swish-appen (alla fälten fylls i automatiskt). Om du
                  precis redan har Swishat så kan det ta ett tag innan vi
                  manuellt registrerar betalningen.
                </p>
                <p>
                  <i>
                    Kontrolluppgifter: Telefonumret är <b>+46 73 033 31 85</b>.
                    Mottagare i BankID ska stå som <b>Vilhelm Prytz</b>{" "}
                    (ekonomiansvarig).
                  </i>
                </p>
              </div>
            </div>
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={handleClose}>
              Stäng
            </Button>
          </Modal.Footer>
        </Modal>
      </Container>
    </OverlayTrigger>
  );
}

export default SeatModal;
