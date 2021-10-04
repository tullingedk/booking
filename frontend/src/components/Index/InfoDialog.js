import React, { useState, useEffect, useRef } from "react";

// material-ui
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import Typography from "@material-ui/core/Typography";

// redux
import { useSelector } from "react-redux";

function InfoDialog() {
  const [open, setOpen] = useState(false);
  const event = useSelector((state) => state.event);

  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const descriptionElementRef = useRef(null);
  useEffect(() => {
    if (open) {
      const { current: descriptionElement } = descriptionElementRef;
      if (descriptionElement !== null) {
        descriptionElement.focus();
      }
    }
  }, [open]);

  return (
    <div>
      <Button variant="outlined" color="primary" onClick={handleClickOpen}>
        Information
      </Button>
      <Dialog
        open={open}
        onClose={handleClose}
        scroll="paper"
        aria-labelledby="scroll-dialog-title"
        aria-describedby="scroll-dialog-description"
      >
        <DialogTitle id="scroll-dialog-title">
          Information om LAN:et
        </DialogTitle>
        <DialogContent dividers={true}>
          <DialogContentText
            id="scroll-dialog-description"
            ref={descriptionElementRef}
            tabIndex={-1}
          >
            <i>
              Kontakta någon i styrelsen via Discord/Vklass ifall du har några
              frågor!
            </i>
            <Typography variant="h4">Bokningen</Typography>
            <Typography gutterBottom={true} variant="h6">
              Hur du bokar
            </Typography>

            <Typography gutterBottom={true}>
              1. Använd bokningsknapparna för att boka en plats. När du fyllt i
              bokningen och skickat den kommer du kunna trycka på din bokning i
              systemet.
            </Typography>
            <Typography gutterBottom={true}>
              2. Öppna Swish-appen och tryck på "Swisha". Längst upp kan du
              trycka för att öppna skanningsläget i Swish. Du kan nu skanna
              koden som visas i bokningssystemet, så ska Swish automatiskt fylla
              i telefonnumer, belopp och ditt namn & klass.
            </Typography>
            <Typography gutterBottom={true}>
              3. Klart! Det kan ta ett tag innan vi manuellt uppdaterar statusen
              på din bokning (från gult till rött).
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Betalningsinformation
            </Typography>

            <Typography gutterBottom={true}>
              Har du problem med att använda QR-koden går det bra att Swisha
              direkt till telefonnummret. Glöm inte att ange namn och klass
              (gärna plats också) i meddelandet!
            </Typography>
            <Typography gutterBottom={true}>
              Mottagare ska vara <b>{event.swish_phone}</b>, belopp ska vara{" "}
              <b>50 kr</b> för vanlig plats och <b>30 kr</b> för en konsol- och
              brädspelsplats. Ange ditt namn och klass i meddelandet.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Städhjälp
            </Typography>
            <Typography gutterBottom={true}>
              Stannar du kvar och hjälper till med att städa efter LANet får du
              tillbaka hela bokningavgiften.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Vid problem / kontakt
            </Typography>
            <Typography gutterBottom={true}>
              Om du har problem med bokningen eller om du vill ändra din
              bokning, kontakta {event.swish_name} (ekonomiansvarig) via
              Discord/Vklass eller föreningen via{" "}
              <a href="mailto:info@tgdk.se">mail</a>. Swishtelefonnumret går
              inte att ringa/SMSa till. Mottagare i BankID ska stå som{" "}
              <i>{event.swish_name}</i>.
            </Typography>

            <Typography gutterBottom={true} variant="h4">
              FAQ
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              När är det?
            </Typography>
            <Typography gutterBottom={true}>
              LANet är {event.event_date}.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Var är det?
            </Typography>
            <Typography gutterBottom={true}>Matsalen.</Typography>

            <Typography gutterBottom={true} variant="h6">
              När får jag komma?
            </Typography>
            <Typography gutterBottom={true}>
              Du är välkommen att komma tidigast 17:00. Respektera dock att
              allting inte nödvändigtvis är klart då.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Vad ska jag ha med mig?
            </Typography>
            <Typography gutterBottom={true}>
              Vill du spela på en dator får du ta med dig en egen dator och
              lämpliga tillbehör. Vill du spela på en konsol får du ta med dig
              en egen konsol och lämplig övrig utrustning. Vi tillhandahåller
              inga skärmar/möss/datorer etc. Vill du ta med dig något att
              äta/dricka får du göra det. Det kommer dock finnas en cafeteria
              där med både lättare mat, dryck och godsaker. Vi ser gärna att du
              tar med dig en egen stol om möjligt då det råder en smärre brist
              på stolar och vi kan inte garantera att alla får låna en stol. Om
              du får låna en stol av skolan är det inte säkert att det blir den
              skönaste eller mest ergonomiska stolen (lösning: ta med en kudde
              att sitta på).
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Vad ska jag inte ha med mig?
            </Typography>
            <Typography gutterBottom={true}>
              Enligt skolans regler FÅR DU INTE TA MED DIG NÖTTER då det finns
              elever som är allergiska mot nötter. Saker som innehåller spår av
              nötter är dock okej. På grund av utrymmesbrist får du inte ta med
              dig mer än en skärm. Du får heller inte ta med dig någon form av
              minifrys/minikyl. <b>NOLLTOLERANS MOT ALKOHOL OCH DROGER</b>.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Kan jag lägga ut bilder på sociala medier?
            </Typography>
            <Typography gutterBottom={true}>
              Eftersom det kommer finnas en hel del utrustning koncentrerad på
              ett ställe uppskattar vi om ni kan vara försiktiga med användandet
              och inte lägga upp bilder på datorer och annan utrustning samt
              inte tagga en plats.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Kan mina vänner komma?
            </Typography>
            <Typography>
              LAN:et är bara öppet för personer med anknytning till skolan.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Skylarooooos point
            </Typography>
            <Typography gutterBottom={true}>
              För de som tänkt sova, vilket kan vara bra för alla att göra minst
              en gång, kommer detta ske i biblioteket där mattor från
              idrottssalen att tas in. Det går att låna dessa mattor eller ta
              med egen madrass/sovsäck. Det kan vara bra för alla att åtminstone
              ta med en kudde och filt eller liknande då golvet (även med
              mattor) är hårt och kallt att ligga på. I biblioteket har vi en
              inga-skor-policy, samt att det skall vara tyst från det att man
              öppnar dörren för att gå in till dess att man gått ut, då det kan
              finnas de som sover oavsett tid på dygnet. Det går även att sova
              på övervåningen, men ej inne i kontoret. Vi skulle även uppskatta
              om sovandet är limiterat till era datorplatser eller biblioteket,
              ifall olyckan skulle vara framme, blir det lättare för oss att
              utrymma om vi vet vart alla som kanske inte märker faran är.
            </Typography>

            <Typography gutterBottom={true} variant="h6">
              Checklista
            </Typography>
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

            <Typography gutterBottom={true} variant="h6">
              Skillnaden mellan platser på LANet
            </Typography>
            <Typography>
              Datorspelsplats: Bordsplacering med plats för dator, stol och
              skärm under hela LAN-et. Har du konsol med dig måste du boka
              Datorplats och ha med dig skärm. Brädspelsplats: Ingen specifik
              plats. Det kommer finnas bord att spela brädspel på och eller
              kort/rollspel. Tillgång till några spelkonsoler som står
              uppställda i biblioteket.
            </Typography>

            <Typography gutterBottom={true} variant="h4">
              Personuppgifter
            </Typography>
            <Typography gutterBottom={true}>
              Denna sida använder en cookie för att hantera inloggningen.
              Bokningsuppgifter lagras i en skyddad databas som raderas efter
              eventets datum. Anslutningen till sidan är krypterad med HTTPS.
              När du bokar en plats kommer uppgifter som namn, klass,
              e-postadress och IP-adress att lagras i databasen. Namn och klass
              visas synligt för alla som har åtkomst till sidan. Inga
              personuppgifter delas aktivt med tredjepart. Namn och klass
              används för bokningen. E-postadressen och IP-adressen hanteras
              automatiskt av systemet i syfte att förhindra spam. Vid avbokning
              raderas eventuella personuppgifter permanent.
              Personuppgiftsansvarig för bokningar gjorda på tgdk.se
              (booking.tgdk.se) är den ideella föreningen TULLINGE GYMNASIUM
              DATORKLUBB med org.nr. 802530-4208. Kontakta{" "}
              <a href="mailto:info@tgdk.se">info@tgdk.se</a> vid frågor.
            </Typography>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            Stäng
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}

export default InfoDialog;
