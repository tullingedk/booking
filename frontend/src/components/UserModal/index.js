import React, { useState, useEffect } from "react";
import Cookies from "js-cookie";
import { Modal, Button } from "react-bootstrap";

import backend_url from "./../../global_variables";

function reload() {
  window.location.reload();
}

function UserModal(props) {
  const [show, setShow] = useState(props.show_modal);

  const [schoolClass, setSchoolClass] = useState("");
  const [password, setPassword] = useState("");

  const [status, setStatus] = useState(false);
  const [statusColor, setStatusColor] = useState("green");

  useEffect(() => {
    setShow(props.show_modal);
  }, [props.show_modal]);

  const handleSubmit = (e) => {
    if (e) {
      e.preventDefault();
    }

    fetch(`${backend_url}/backend/google_callback`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        idtoken: props.idtoken,
        create: true,
        class: schoolClass,
        password: password,
      }),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          if (response.status === 502) {
            setStatus(
              "Ett fel uppstod, kunde inte kommunicera med server. Kontakta Prytz via Discord om problemet kvarstår."
            );
            setStatusColor("red");
          } else {
            // other errors are handled by json
            return response.json();
          }
        }
      })
      .then((json) => {
        console.log(json.http_code + json.message);
        setStatusColor("red");

        if (json.http_code === 400) {
          setStatus(json.message);
        } else if (json.http_code === 500) {
          setStatus(json.message);
        } else if (json.http_code === 401) {
          setStatus(json.message);
        } else if (json.http_code === 429) {
          setStatus(
            "Du har skickat för många anrop. Kontakta Prytz via Discord om problemet kvarstår."
          );
        } else if (json.http_code === 200 && json.status) {
          // set session
          Cookies.set("session_token", json.response.session, {
            expires: 7,
            path: "/",
          });

          Cookies.set("email", json.response.email, {
            expires: 7,
            path: "/",
          });

          Cookies.set("name", json.response.name, {
            expires: 7,
            path: "/",
          });

          Cookies.set("school_class", json.response.school_class, {
            expires: 7,
            path: "/",
          });
          reload();
        }
      });
  };

  return (
    <div>
      <Modal show={show}>
        <Modal.Header>
          <Modal.Title>Registrera användare</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            <p className="formText">
              Din användare är inte registrerad. Använd formuläret nedan för att
              registrera ditt konto till en klass.
            </p>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Klass</label>
                <input
                  className="form-control"
                  onChange={(e) => setSchoolClass(e.target.value)}
                  value={schoolClass}
                  type="text"
                  name="school_class"
                  required
                />
              </div>

              <div className="form-group">
                <label>Lösenord</label>
                <input
                  className="form-control"
                  onChange={(e) => setPassword(e.target.value)}
                  value={password}
                  type="password"
                  name="password"
                  required
                />
                <small id="passwordHelp" class="form-text text-muted">
                  Detta är lösenordet som du fått från Datorklubben (för att
                  verifiera att endast elever på skolan hat åtkomst till
                  systemet). Det är alltså inte ditt egna lösenord!
                </small>
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
          <Button variant="danger" onClick={reload}>
            Avbryt
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default UserModal;
