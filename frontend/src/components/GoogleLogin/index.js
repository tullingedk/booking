import React, { useState } from "react";
import Cookies from "js-cookie";
import styled from "styled-components";
import Konami from "react-konami-code";
import { GoogleLogin, useGoogleLogout } from "react-google-login";

import UserModal from "../UserModal/index";

import backend_url from "./../../global_variables";

const Title = styled.h1``;

const Text = styled.p``;

const Container = styled.div`
  padding: 1em;
  width: 95%;
  margin: auto;
  text-align: center;
`;

function Login(props) {
  const [status, setStatus] = useState("");
  const [statusColor, setStatusColor] = useState("");
  const [userCreateModal, setUserCreateModal] = useState(false);
  const [userCreateTokenId, setUserCreateTokenId] = useState("");

  const { signOut } = useGoogleLogout({});

  const responseGoogle = (response) => {
    var id_token = response.tokenId;

    fetch(`${backend_url}/backend/google_callback`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        idtoken: id_token,
        create: false,
      }),
    })
      .then(function (response) {
        if (
          response.status === 200 ||
          response.status === 400 ||
          response.status === 401
        ) {
          return response.json();
        } else {
          signOut();
          setStatus("Ett fel uppstod. Fel: " + response.status);
          setStatusColor("red");
        }
      })
      .then(function (json) {
        if (json.status) {
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

          // redirect
          window.location.replace("/");
        } else {
          if (json.response.configure_user) {
            setUserCreateTokenId(id_token);
            setUserCreateModal(true);
          } else {
            signOut();
            setStatus("Ett fel uppstod. Fel: " + json.message);
            setStatusColor("red");
          }
        }
      });
  };

  return (
    <div className="App">
      <Container>
        <Title>Datorklubben Bokningssystem - Inloggning</Title>
        <Text>Logga in med ditt skolkonto.</Text>
        <Text>Denna sida använder en cookie för att hantera inloggningen.</Text>

        <GoogleLogin
          clientId={props.info_json.google_clientid}
          buttonText="Login"
          onSuccess={responseGoogle}
          onFailure={responseGoogle}
          cookiePolicy={"single_host_origin"}
        />
        <p style={{ color: statusColor }} className="status">
          {status}
        </p>
      </Container>
      <Konami
        action={() => {
          window.location.href = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
        }}
      />
      <UserModal show_modal={userCreateModal} idtoken={userCreateTokenId} />
    </div>
  );
}

export default Login;
