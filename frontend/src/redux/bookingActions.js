export const OPEN_BOOKING_DIALOG = "OPEN_BOOKING_DIALOG";
export const FETCH_BOOKINGS_BEGIN = "FETCH_BOOKINGS_BEGIN";
export const FETCH_BOOKINGS_SUCCESS = "FETCH_BOOKINGS_SUCCESS";
export const FETCH_BOOKINGS_FAILURE = "FETCH_BOOKINGS_FAILURE";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

export const setBookingDialog = (dialog_open, dialog_id, dialog_seat_type) => ({
  type: OPEN_BOOKING_DIALOG,
  payload: { dialog_open, dialog_id, dialog_seat_type },
});

export const fetchBookingsBegin = () => ({
  type: FETCH_BOOKINGS_BEGIN,
});

export const fetchBookingsSuccess = (bookings, console_bookings) => ({
  type: FETCH_BOOKINGS_SUCCESS,
  payload: { bookings, console_bookings },
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
        dispatch(
          fetchBookingsSuccess(
            json.response.bookings,
            json.response.console_bookings
          )
        );
        return json.response;
      })
      .catch((error) => {
        console.error(error);
        dispatch(fetchBookingsFailure(error));
      });
  };
}

// Handle HTTP errors since fetch won't.
function handleErrors(response) {
  if (!response.ok) {
    const contentType = response.headers.get("content-type");
    if (contentType && contentType.indexOf("application/json") !== -1) {
      return response.json().then((json) => {
        throw Error(
          `${response.statusText}: ${json.message} (${response.status})`
        );
      });
    } else {
      throw Error(response.statusText);
    }
  }
  return response;
}
