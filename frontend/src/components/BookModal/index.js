import React, { useState, useEffect } from "react";
import { Modal, Button } from "react-bootstrap";
import {
  NotificationContainer,
  NotificationManager
} from "react-notifications";
import "react-notifications/lib/notifications.css";

import backend_url from "./../../global_variables";

function BookModal(props) {
  const [show, setShow] = useState(false);
  const handleClose = () => setShow(false);

  const [name, setName] = useState("");
  const [schoolClass, setSchoolClass] = useState("");
  const [email, setEmail] = useState("");
  const [seat, setSeat] = useState();

  const [status, setStatus] = useState(false);
  const [statusColor, setStatusColor] = useState("green");

  const [availableSeatList, setAvailableSeatList] = useState("");

  useEffect(() => {
    fetch(`${backend_url}/backend${props.available_seat_list_url}`, {
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
            setStatus(
              "Ett fel uppstod, kunde inte kommunicera med server. Kontakta Prytz via Discord om problemet kvarstår."
            );
            setStatusColor("red");
            throw new Error("Kunde inte kommunicera med server.");
          } else {
            // other errors are handled by json
            return response.json();
          }
        }
      })
      .then(json => {
        if (json.http_code === 200) {
          setAvailableSeatList(json.response.available_seat_list);
          setSeat(availableSeatList[0]);
        } else {
          setStatus(
            "Ett fel uppstod, kunde inte kommunicera med server. Kontakta Prytz via Discord om problemet kvarstår."
          );
          setStatusColor("red");
        }
      });
  }, [show, props.session_token, props.available_seat_list_url]);

  const handleSubmit = e => {
    if (e) {
      e.preventDefault();
    }

    fetch(`${backend_url}/backend${props.request_url}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        token: props.session_token,
        name: name,
        class: schoolClass,
        email: email,
        seat: seat
      })
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          if (response.status === 502) {
            setStatus(
              "Ett fel uppstod, kunde inte kommunicera med server. Kontakta Prytz via Discord om problemet kvarstår."
            );
            setStatusColor("red");
            throw new Error("Kunde inte kommunicera med server.");
          } else {
            // other errors are handled by json
            return response.json();
          }
        }
      })
      .then(json => {
        console.log(json.http_code + json.message);
        setStatusColor("red");

        if (json.http_code === 400) {
          setStatus(json.message);
        } else if (json.http_code === 500) {
          setStatus(json.message);
        } else if (json.http_code === 401) {
          setStatus("Din session har gått ut. Ladda om sidan.");
        } else if (json.http_code === 429) {
          setStatus(
            "Du har skickat för många anrop. Kontakta Prytz via Discord om problemet kvarstår."
          );
        } else if (json.http_code === 201) {
          NotificationManager.success(
            "Din bokning är nu sparad",
            "Bokningen lyckades"
          );
          setName("");
          setSchoolClass("");
          setEmail("");
          setSeat("");
          setStatus("");
          setShow(false);
        }
      });
  };

  return (
    <div>
      <Button style={{ margin: "0.15em" }} onClick={() => setShow(true)}>
        {props.button_text}
      </Button>

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
                <input
                  className="form-control"
                  onChange={e => setName(e.target.value)}
                  value={name}
                  type="text"
                  name="name"
                  required
                />
              </div>

              <div className="form-group">
                <label>Klass</label>
                <input
                  className="form-control"
                  onChange={e => setSchoolClass(e.target.value)}
                  value={schoolClass}
                  type="text"
                  name="school_class"
                  required
                />
              </div>

              <div className="form-group">
                <label>E-mail</label>
                <input
                  className="form-control"
                  onChange={e => setEmail(e.target.value)}
                  value={email}
                  type="email"
                  name="email"
                  required
                />
                <small id="emailHelp" class="form-text text-muted">
                  Du måste ange din skolmailadress. Detta är för att förhindra
                  spam.
                </small>
              </div>

              <div className="form-group">
                <label>Plats</label>

                <select
                  className="form-control"
                  value={seat}
                  onChange={e => setSeat(e.target.value)}
                  required
                  name="seat"
                >
                  {Array.from(availableSeatList).map(function(object) {
                    return <option value={object}>{object}</option>;
                  })}
                </select>
              </div>

              <button type="submit" className="btn btn-primary">
                Skicka
              </button>
            </form>

            <p style={{ color: statusColor }} className="status">
              {status}
            </p>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Stäng
          </Button>
        </Modal.Footer>
      </Modal>
      <NotificationContainer />
    </div>
  );
}

export default BookModal;
