import {
  FETCH_BOOKINGS_BEGIN,
  FETCH_BOOKINGS_SUCCESS,
  FETCH_BOOKINGS_FAILURE,
} from "../bookingActions";

const initialState = {
  bookings: [],
  console_bookings: [],
  loading: false,
  error: null,
};

function bookingReducer(state = initialState, action) {
  switch (action.type) {
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
