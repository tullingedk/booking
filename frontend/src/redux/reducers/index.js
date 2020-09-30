import { combineReducers } from "redux";

// import reducers
import {
  user,
  isAuthenticated,
  isRegistered,
  systemMeta,
  event,
} from "./basicReducers";
import bookingReducer from "./bookingReducer";

export default combineReducers({
  user,
  isAuthenticated,
  isRegistered,
  systemMeta,
  bookingReducer,
  event,
});
