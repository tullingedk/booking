import React, { useState, useEffect } from "react";
import { Modal, Button } from "react-bootstrap";

function reload() {
  window.location.reload();
}

function ErrorModal(props) {
  const [show, setShow] = useState(props.show_modal);

  useEffect(() => {
    setShow(props.show_modal);
  }, [props.show_modal]);

  return (
    <div>
      <Modal show={show}>
        <Modal.Header>
          <Modal.Title>Ett fel uppstod</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div>
            <p>
              Ett fel uppstod vid anslutningen till servern. Kontakta Prytz via
              Discord om problemet kvarstår.
            </p>
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="primary" onClick={reload}>
            Ladda om sidan
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default ErrorModal;
