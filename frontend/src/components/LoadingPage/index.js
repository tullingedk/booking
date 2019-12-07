import React from "react";
import styled from "styled-components";

const Container = styled.div`
  padding: 1em;
  width: 100%;
  margin: auto;
  text-align: center;
`;

function DisabledPage() {
  return (
    <div className="App">
      <Container>
        <h1>Datorklubben Bokningssystem</h1>
        <img alt="Laddar..." src="loading.gif" />
      </Container>
    </div>
  );
}

export default DisabledPage;
