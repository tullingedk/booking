import React, { useState } from 'react';
import styled from 'styled-components';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';

const Title = styled.h1`

`

const Text = styled.p`

`

const LoginForm = styled.form`
    max-width: 50%;
    margin: auto;
    padding: 0;
`

const Container = styled.div`
    padding: 1em;
    width: 100vmin;
    margin: auto;
    text-align: center;
`

function Login() {
    const [password, setPassword] = useState("");

    const [status, setStatus] = useState ("");
    const [statusColor, setStatusColor] = useState("");

    const handleSubmit = (e) => {
        if (e) { e.preventDefault(); }

        fetch('https://booking.vilhelmprytz.se/backend/auth', {
            method: "POST",
            headers: {
                "Accept": 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                password: password,
            })
        })
        .then(response => response.json())
        .then(data => {
            setStatusColor("red");
            if (data.status === 201) {
              console.log(data.message);

              // clear variable
              setPassword("");

              // should set session cookie and redirect
            } else if (data.status === 429) {
              console.log(data.message)
              setStatus("Du har skickat för många anrop, vänta en stund innan du försöker igen. Om problemet kvarstår, kontakta Prytz via Discord.");
            } else if (data.status === 400) {
              console.log(data.message);
              setStatus(data.message);
            } else if (data.status === 502) {
              console.log("bad gateway, backend is down!")
              setStatus("Något fungerar inte med våra servrar. Om problemet kvarstår, kontakta Prytz via Discord.")
            } else {
              console.log(data.message);
              setStatus("Okänt fel inträffat (felkod " + data.status + "): " + data.message);
            }
        })
    };

    const validateForm = () => {
        return password.length >= 3 && password.length < 50;
    };

    return (
        <Container>
            <Title>Datorklubben Bokningssystem - Inloggning</Title>
            <Text>För att förhindra spamm krävs ett lösenord.</Text>

            <LoginForm onSubmit={handleSubmit}>
                <Form.Group controlId="password">
                <Form.Control
                    value={password}
                    onChange={e => setPassword(e.target.value)}
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
            <p style={{color: statusColor}} className="status">{status}</p>
        </Container>
    )
}

export default Login