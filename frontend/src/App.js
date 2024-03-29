import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";

// pages
import Index from "./pages/Index";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Error from "./pages/Error";

// redux
import { setAuthenticated } from "./redux/actions";
import { setRegistered } from "./redux/actions";
import { setUserEmail } from "./redux/actions";
import { setUserName } from "./redux/actions";
import { setUserClass } from "./redux/actions";
import { setUserAvatar } from "./redux/actions";
import { setVersion } from "./redux/actions";
import { setHash } from "./redux/actions";
import { setHashDate } from "./redux/actions";
import { setIsAdmin } from "./redux/actions";
import {
  setEventDate,
  setEventSwishName,
  setEventSwishPhone,
} from "./redux/actions";

// redux bookings
import { fetchBookings } from "./redux/bookingActions";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const dispatch = useDispatch();

  const isAuthenticated = useSelector((state) => state.isAuthenticated);
  const isRegistered = useSelector((state) => state.isRegistered);

  const [error, setError] = useState("");

  useEffect(() => {
    fetch(`${BACKEND_URL}/api/auth/validate`, {
      credentials: "include",
    })
      .then((response) => response.json())
      .then((data) => {
        // set meta
        // should be included at all times
        dispatch(setVersion(data.meta.version));
        dispatch(setHash(data.meta.commit_hash));
        dispatch(setHashDate(data.meta.commit_date));

        if (data.http_code === 200) {
          // if 200, all is good
          dispatch(setAuthenticated(true));
          dispatch(setRegistered(true));

          // set user info
          dispatch(setUserEmail(data.response.email));
          dispatch(setUserName(data.response.name));
          dispatch(setUserClass(data.response.school_class));
          dispatch(setUserAvatar(data.response.avatar));
          dispatch(setIsAdmin(data.response.is_admin));

          // set event data
          dispatch(setEventDate(data.response.event.event_date));
          dispatch(setEventSwishName(data.response.event.swish_name));
          dispatch(setEventSwishPhone(data.response.event.swish_phone));

          // initial data fetch
          dispatch(fetchBookings());
        } else if (data.http_code === 401) {
          if (data.response.google === true) {
            // if is authenticated with google
            dispatch(setAuthenticated(true));
          }
          if (data.response.registered === true) {
            // if is registered
            dispatch(setRegistered(true));
          }
        } else {
          setError(`Ett fel uppstod: ${data.message}`);
        }
      })
      .catch((e) => {
        setError(`Ett fel uppstod: ${e}`);
      });
  }, [dispatch]);

  if (error) {
    return <Error error={error} />;
  }

  if (isAuthenticated && isRegistered) {
    return <Index />;
  } else {
    if (isAuthenticated) {
      return <Register />;
    } else {
      return <Login />;
    }
  }
}

export default App;
