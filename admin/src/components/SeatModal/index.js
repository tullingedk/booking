import React, { useState, useEffect } from 'react';
import { Modal, Button, Tooltip, OverlayTrigger } from 'react-bootstrap';
import {NotificationContainer, NotificationManager} from 'react-notifications';
import 'react-notifications/lib/notifications.css';
import styled from 'styled-components';

import backend_url from './../../global_variables';

const Container = styled.div`
    background-color: white;
`

const Seat = styled.div`
    border-style: solid;
    margin: auto;
    width: 3em;
    height: 3em;
`

const Text = styled.p`
    margin: auto;
    padding: 0px;
`

function SeatModal(props) {
    const [show, setShow] = useState(false);
    const [blockShow, setBlockShow] = useState(true);
    const [cursor, setCursor] = useState("");
    const handleClose = () => setShow(false);
    const handleShow = () => {
        if (blockShow === false) {
            setShow(true);
        }
    }

    const [seatType, setSeatType] = useState(false);
    const [seatColor, setSeatColor] = useState("white");
    const [name, setName] = useState("");
    const [schoolClass, setSchoolClass] = useState("");
    const [date, setDate] = useState("");
    const [bookingStatus, setBookingStatus] = useState("");

    const handlePaid = (e) => {
        if (e) { e.preventDefault(); }
        handleSubmit(true);
    }

    const handleUnpaid = (e) => {
        if (e) { e.preventDefault(); }
        handleSubmit(false);
    }

    const handleSubmit = (action) => {
        fetch(`${backend_url}/backend/admin${seatType ? '/' : '/bc/' }${action ? 'paid' : 'unpaid'}/${props.id}`, {
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
                if (response.status === 502) {
                    NotificationManager.error("Kunde inte kommunicera med server", 'Ett fel uppstod');
                    throw new Error('Kunde inte kommunicera med server.');
                } else {
                    // other errors are handled by json
                    return response.json();
                }

            }
        })
        .then((json) => {
            console.log(json.http_code + json.message)

            if (json.http_code === 400) {
                NotificationManager.error(json.message, 'Ett fel uppstod');
            } else if (json.http_code === 500) {
                NotificationManager.error(json.message, 'Ett fel uppstod');
            } else if (json.http_code === 401) {
                NotificationManager.error(json.message, 'Ett fel uppstod');
            } else if (json.http_code === 200) {
                NotificationManager.success('Ändringen är sparad', 'Statusändring lyckades');
            }
        });
    };

    useEffect(() => {
        var booking = Array.from(props.bookings).filter(obj => {
            return obj.id === props.id;
        })
    
        if (booking.length !== 0) { booking = booking[0]; };
    
        if (parseInt(booking.status) === 1) {
            setSeatColor("yellow");
            setBlockShow(false);
            setCursor("pointer");
            setBookingStatus("Obetald");
        } else if (parseInt(booking.status) === 0) {
            setSeatColor("red");
            setBlockShow(false);
            setCursor("pointer");
            setBookingStatus("Betald");
        }

        setName(booking.name);
        setSchoolClass(booking.school_class);
        setDate(booking.date);

    }, [props.bookings, props.id]);

    useEffect(() => {
        if (props.seat_type) {
            setSeatType(true);
        }
    }, [props.seat_type])

    return (
        <OverlayTrigger
            placement="top"
            delay={{ show: 250, hide: 400 }}
            overlay={            
                <Tooltip style={{display: blockShow ? 'none' : 'block' }} id={props.id}>
                    {name} {schoolClass}
                </Tooltip>
            }
        >
            <Container style={{backgroundColor: seatColor, cursor: cursor}}>
                <Seat onClick={handleShow}>{props.children}</Seat>

                <Modal show={show} onHide={handleClose}>
                    <Modal.Header closeButton>
                    <Modal.Title>{seatType ? 'Plats' : 'Konsol- och brädspelssplats' } {props.id}</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                    <div>
                        <Text>Namn: {name}</Text>
                        <Text>Klass: {schoolClass}</Text>
                        <Text>Bokades: {date}</Text>
                        <Text>Status: {bookingStatus}</Text>

                        <form onSubmit={handlePaid}>
                            <Button style={{margin: "0.15em"}} type="submit">Markera som betald</Button>
                        </form>
                        <form onSubmit={handleUnpaid}>
                            <Button style={{margin: "0.15em"}} type="submit">Markera som obetald</Button>
                        </form>
                    </div>
                    </Modal.Body>
                    <Modal.Footer>
                    <Button variant="secondary" onClick={handleClose}>
                        Stäng
                    </Button>
                    </Modal.Footer>
                </Modal>
                <NotificationContainer />
            </Container>
        </OverlayTrigger>
    )
}

export default SeatModal;