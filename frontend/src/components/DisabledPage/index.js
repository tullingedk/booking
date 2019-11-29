import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
    padding: 1em;
    width: 100vmax;
    margin: auto;
    text-align: center;
`

function DisabledPage() {
    return (
        <div className="App">
            <Container>
                <h1>Datorklubben Bokningssystem</h1>
                <p>Tack för denna gång. Bokingssystemet är nu stängt men kommer att öppna innan nästa LAN.</p>
            </Container>
        </div>
    )
}

export default DisabledPage;