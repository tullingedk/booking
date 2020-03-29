import React, { useState } from "react";
import Cookies from "js-cookie";
import styled from "styled-components";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Konami from "react-konami-code";

import backend_url from "./../../global_variables";

const Title = styled.h1``;

const Text = styled.p``;

const LoginForm = styled.form`
  width: 100%;
  max-width: 400px;
  margin: auto;
  padding: 0;
`;

const Container = styled.div`
  padding: 1em;
  width: 95%;
  margin: auto;
  text-align: center;
`;

function Login() {
  const [password, setPassword] = useState("");

  const [status, setStatus] = useState("");
  const [statusColor, setStatusColor] = useState("");

  const handleSubmit = (e) => {
    if (e) {
      e.preventDefault();
    }

    fetch(`${backend_url}/backend/auth`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        password: password,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setStatusColor("red");
        if (data.status === true) {
          console.log(data);

          // clear variable
          setPassword("");

          // set session
          Cookies.set("session_token", data.response.session, {
            expires: 7,
            path: "/",
          });

          // redirect
          window.location.replace("/");
        } else if (data.http_code === 429) {
          console.log(data);
          setStatus(
            "Du har skickat för många anrop, vänta en stund innan du försöker igen. Om problemet kvarstår, kontakta Prytz via Discord."
          );
        } else if (data.http_code === 400) {
          console.log(data);
          setStatus(data.message);
        } else if (data.http_code === 401) {
          console.log(data);
          setStatus(data.message);
        } else if (data.http_code === 502) {
          console.log("bad gateway, backend is down!");
          setStatus(
            "Något fungerar inte med våra servrar. Om problemet kvarstår, kontakta Prytz via Discord."
          );
        } else {
          console.log(data);
          setStatus(
            "Okänt fel inträffat (felkod " +
              data.http_code +
              "): " +
              data.message
          );
        }
      });
  };

  const validateForm = () => {
    return password.length >= 3 && password.length < 200;
  };

  return (
    <div className="App">
      <Container>
        <Title>Datorklubben Bokningssystem - Inloggning</Title>
        <Text>För att förhindra spam krävs ett lösenord.</Text>
        <Text>Denna sida använder en cookie för att hantera inloggningen.</Text>

        <LoginForm onSubmit={handleSubmit}>
          <Form.Group controlId="password">
            <Form.Control
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              type="password"
              placeholder="Lösenord"
              name="password"
              required
            />
          </Form.Group>
          <Button block disabled={!validateForm()} type="submit">
            Skicka
          </Button>
        </LoginForm>
        <p style={{ color: statusColor }} className="status">
          {status}
        </p>
      </Container>
      <Konami
        action={() => {
          window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
        }}
      />
    </div>
  );
}

export default Login;
