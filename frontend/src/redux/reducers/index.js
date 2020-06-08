import { combineReducers } from "redux";

function isAuthenticated(authenticated = false, action) {
  switch (action.type) {
    case "SET_AUTHENTICATED":
      return action.authenticated;
    default:
      return authenticated;
  }
}

function userEmail(email = "", action) {
  switch (action.type) {
    case "USER_SET_EMAIL":
      return action.email;
    default:
      return email;
  }
}

export default combineReducers({ userEmail, isAuthenticated });
