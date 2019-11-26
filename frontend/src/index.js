import React from 'react';
import ReactDOM from 'react-dom';
import Cookies from 'js-cookie';
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

import Login from './components/Login/index';
import DisabledPage from './components/DisabledPage/index';

import backend_url from './global_variables';


fetch(`${backend_url}/backend/info`)
.then((response) => {
    if(response.ok) {
        return response.json();
    } else {
        throw new Error('Kunde inte kommunicera med server.');
    }
})
.then((json) => {
    console.log(json);

    let Routing = App;
    if (json.response.disabled) {
        Routing = DisabledPage;
    } else {
        // check for auth
        if (Cookies.get("session_token")) {
            fetch(`${backend_url}/backend/validate_session`, {
                method: "POST",
                headers: {
                    "Accept": 'application/json',
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    token: Cookies.get("session_token"),
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data)

                if (data.status === false) {
                    Cookies.remove('session_token');
                    window.location.replace("/");
                }
            });
        } else {
            Routing = Login;
        }
    }

    ReactDOM.render(<Routing info_json={json} session_token={Cookies.get("session_token")} />, document.getElementById('root')); 
});

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
