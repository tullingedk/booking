import {
  OPEN_BOOKING_DIALOG,
  FETCH_BOOKINGS_BEGIN,
  FETCH_BOOKINGS_SUCCESS,
  FETCH_BOOKINGS_FAILURE,
} from "../bookingActions";

const initialState = {
  bookings: [],
  console_bookings: [],
  loading: false,
  error: null,
  dialog_open: false,
  dialog_id: null,
  dialog_seat_type: null,
  num_seats: null,
  num_console_seats: null,
};

function bookingReducer(state = initialState, action) {
  switch (action.type) {
    case OPEN_BOOKING_DIALOG:
      return {
        ...state,
        dialog_open: action.payload.dialog_open,
        dialog_id: action.payload.dialog_id,
        dialog_seat_type: action.payload.dialog_seat_type,
      };

    case FETCH_BOOKINGS_BEGIN:
      return {
        ...state,
        loading: true,
        error: null,
      };

    case FETCH_BOOKINGS_SUCCESS:
      return {
        ...state,
        loading: false,
        bookings: action.payload.bookings,
        console_bookings: action.payload.console_bookings,
        num_seats: action.payload.num_seats,
        num_console_seats: action.payload.num_console_seats,
      };

    case FETCH_BOOKINGS_FAILURE:
      return {
        ...state,
        loading: false,
        error: `${action.payload.error}`,
      };

    default:
      // reducer should always have a default!
      return state;
  }
}

export default bookingReducer;
