import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import styled from 'styled-components';

import backend_url from './../../global_variables';

let seat_list = [];
for (var i = 0; i < 61; i++) { seat_list.push(i); };

function BookModal(props) {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [seat, setSeat] = useState("");

    const [status, setStatus] = useState(false);
    const [statusColor, setStatusColor] = useState("green");

    const handleSubmit = (e) => {
        if (e) { e.preventDefault(); }

        fetch(`${backend_url}/backend${props.request_url}`, {
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
                setStatus("Ett fel uppstod, kunde inte kommunicera med server.");
                setStatusColor("red");
                throw new Error('Kunde inte kommunicera med server.');
            }
        })
        .then((json) => {
            window.location.replace("/");
        });
    };

    return (
        <div>
            <Button onClick={() => setShow(true)}>{props.button_text}</Button>
        
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>{props.modal_title}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                <div>
                    <p className="formText">{props.modal_desc}</p>
                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label>Namn</label>
                            <input className="form-control" onChange={(e) => setName(e.target.value)} value={name} type="text" name="name" required />
                        </div>

                        <div className="form-group">
                            <label>E-mail</label>
                            <input className="form-control" onChange={(e) => setEmail(e.target.value)} value={email} type="email" name="email" required />
                        </div>

                        <div className="form-group">
                            <label>Plats</label>

                            <select className="form-control" required name="seat">
                                {seat_list.map(function(object, i){
                                    return <option value={i}>{i}</option>
                                })}
                            </select>
                        </div>

                        <button type="submit" className="btn btn-primary">Skicka</button>
                    </form>
                    
                    <p style={{color: statusColor}} className="status">{status}</p>
                </div>
                </Modal.Body>
                <Modal.Footer>
                <Button variant="secondary" onClick={handleClose}>
                    Stäng
                </Button>
                </Modal.Footer>
            </Modal>
        </div>
    )
}

export default BookModal;