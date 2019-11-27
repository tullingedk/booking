import React, { useState } from 'react';
import { Modal, Button } from 'react-bootstrap';
import styled from 'styled-components';

const Text = styled.p`
`

const Header = styled.h3`
    font-weight: bold;
`

const SubHeader = styled.h5`
    font-weight: bold;
`

function InfoModal(props) {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);

    return (
        <div>
            <Button style={{margin: "0.15em"}} onClick={() => setShow(true)}>Information</Button>

            <Modal size="lg" show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                <Modal.Title>Information om LANet</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                <div>
                    <p><i>Kontakta någon i styrelsen via Discord ifall du har några frågor!</i></p>

                    <Header>Bokningen</Header>
                    <SubHeader>Hur du bokar</SubHeader>

                    <Text>1. Använd bokningsknapparna för att boka en plats. När du fyllt i bokningen och skickat den kommer du kunna trycka på din bokning i systemet.</Text>
                    <Text>2. Öppna Swish-appen och tryck på "Swisha". Längst upp kan du trycka för att öppna skanningsläget i Swish. Du kan nu skanna koden som visas i bokningssystemet, så ska Swish automatiskt fylla i telefonnumer, belopp och ditt namn & klass.</Text>
                    <Text>3. Klart! Det kan ta ett tag innan vi manuellt uppdaterar statusen på din bokning (från gult till rött).</Text>

                    <SubHeader>Betalningsinformation</SubHeader>

                    <Text>Har du problem med att använda QR-koden går det bra att Swisha direkt till telefonnummret. Glöm inte att ange namn och klass (gärna plats också) i meddelandet!</Text>
                    <Text>Mottagare ska vara <b>073 033 31 85</b>, belopp ska vara <b>100 kr</b> för vanlig plats och <b>50 kr</b> för en konsol- och brädspelsplats. Ange ditt namn och klass i meddelandet.</Text>

                    <SubHeader>Städhjälp</SubHeader>
                    <Text>Stannar du kvar och hjälper till med att städa efter LANet får du tillbaka halva bokningavgiften.</Text>

                    <SubHeader>Vid problem / kontakt</SubHeader>
                    <Text>Om du har problem med bokningen eller om du vill ändra din bokning, kontakta Vilhelm Prytz (ekonomiansvarig) via Discord eller <a href="mailto:vilhelm@prytznet.se">mail</a>. Swishtelefonnumret går inte att ringa/SMSa till. Mottagare i BankID ska stå som <i>VILHELM PRYTZ</i>.</Text>

                    <Header>FAQ</Header>

                    <SubHeader>När är det?</SubHeader>
                    <Text>LANet är {props.event_date}.</Text>

                    <SubHeader>Var är det?</SubHeader>
                    <Text>Matsalen.</Text>

                    <SubHeader>När får jag komma?</SubHeader>
                    <Text>Du är välkommen att komma tidigast 17:00. Respektera dock att allting inte nödvändigtvis är klart då.</Text>

                    <SubHeader>Vad ska jag ha med mig?</SubHeader>
                    <Text>Vill du spela på en dator får du ta med dig en egen dator och lämpliga tillbehör.  Vill du spela på en konsol får du ta med dig en egen konsol och lämplig övrig utrustning. Vi tillhandahåller inga skärmar/möss/datorer etc. Vill du ta med dig något att äta/dricka får du göra det. Det kommer dock finnas en cafeteria där med både lättare mat, dryck och godsaker. Vi ser gärna att du tar med dig en egen stol om möjligt då det råder en smärre brist på stolar och vi kan inte garantera att alla får låna en stol.  Om du får låna en stol av skolan är det inte säkert att det blir den skönaste eller mest ergonomiska stolen (lösning: ta med en kudde att sitta på).</Text>

                    <SubHeader>Vad ska jag inte ha med mig?</SubHeader>
                    <Text>Enligt skolans regler FÅR DU INTE TA MED DIG NÖTTER då det finns elever som är allergiska mot nötter.  Saker som innehåller spår av nötter är dock okej. På grund av utrymmesbrist får du inte ta med dig mer än en skärm. Du får heller inte ta med dig någon form av minifrys/minikyl. <b>NOLLTOLERANS MOT ALKOHOL OCH DROGER</b>.</Text>

                    <SubHeader>Kan jag lägga ut bilder på sociala medier?</SubHeader>
                    <Text>Eftersom det kommer finnas en hel del utrustning koncentrerad på ett ställe uppskattar vi om ni kan vara försiktiga med användandet och inte lägga upp bilder på datorer och annan utrustning samt inte tagga en plats.</Text>

                    <SubHeader>Kan mina vänner komma?</SubHeader>
                    <Text>LAN:et är bara öppet för personer med anknytning till skolan. Besökare är välkomna på lördagen mellan 15:00-19:00 (preliminärt, hör med någon i styrelsen under LANet) om detta först meddelas till en ansvarig.</Text>

                    <SubHeader>Skylarooooos point</SubHeader>
                    <Text>För de som tänkt sova, vilket kan vara bra för alla att göra minst en gång, kommer detta ske i biblioteket där mattor från idrottssalen att tas in. Det går att låna dessa mattor eller ta med egen madrass/sovsäck. Det kan vara bra för alla att åtminstone ta med en kudde och filt eller liknande då golvet (även med mattor) är hårt och kallt att ligga på. I biblioteket har vi en inga-skor-policy, samt att det skall vara tyst från det att man öppnar dörren för att gå in till dess att man gått ut, då det kan finnas de som sover oavsett tid på dygnet. Det går även att sova på övervåningen, men ej inne i kontoret. Vi skulle även uppskatta om sovandet är limiterat till era datorplatser eller biblioteket, ifall olyckan skulle vara framme, blir det lättare för oss att utrymma om vi vet vart alla som kanske inte märker faran är.</Text>

                    <SubHeader>Checklista</SubHeader>
                    <ul>
                        <li>Dator/Konsol</li>
                        <li>Skärm (max 1)</li>
                        <li>Mus</li>
                        <li>Tangentbord</li>
                        <li>Strömkabel till skärm och dator</li>
                        <li>DVI-/VGA-/HDMI-/DP-kabel (kabel mellan skärm och dator)</li>
                        <li>Headset</li>
                        <li>Grenkontakt(er)</li>
                        <li>Musmatta</li>
                        <li>Egen stol (om möjligt)</li>
                        <li>Sovutrustning</li>
                        <li>Ethernetkabel (längsta möjliga, helst >5m)</li>
                        <li>Hygienartiklar (det finns dusch i omklädningsrummet)</li>
                        <li>Snacks (om du inte litar på oss)</li>
                    </ul>
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

export default InfoModal;