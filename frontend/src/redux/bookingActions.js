export const FETCH_BOOKINGS_BEGIN = "FETCH_BOOKINGS_BEGIN";
export const FETCH_BOOKINGS_SUCCESS = "FETCH_BOOKINGS_SUCCESS";
export const FETCH_BOOKINGS_FAILURE = "FETCH_BOOKINGS_FAILURE";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const fetchBookingsBegin = () => ({
  type: FETCH_BOOKINGS_BEGIN,
});

export const fetchBookingsSuccess = (bookings) => ({
  type: FETCH_BOOKINGS_SUCCESS,
  payload: { bookings },
});

export const fetchBookingsFailure = (error) => ({
  type: FETCH_BOOKINGS_FAILURE,
  payload: { error },
});

export function fetchBookings() {
  return (dispatch) => {
    dispatch(fetchBookingsBegin());

    return fetch(`${BACKEND_URL}/api/booking/bookings`, {
      credentials: "include",
    })
      .then(handleErrors)
      .then((res) => res.json())
      .then((json) => {
        dispatch(fetchBookingsSuccess(json.response));
        return json.response;
      })
      .catch((error) => dispatch(fetchBookingsFailure(error)));
  };
}

// Handle HTTP errors since fetch won't.
function handleErrors(response) {
  if (!response.ok) {
    throw Error(response.statusText);
  }
  return response;
}
