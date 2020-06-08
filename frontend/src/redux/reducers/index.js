import { combineReducers } from "redux";

function isAuthenticated(authenticated = false, action) {
  switch (action.type) {
    case "SET_AUTHENTICATED":
      return action.authenticated;
    default:
      return authenticated;
  }
}

function isRegistered(registered = false, action) {
  switch (action.type) {
    case "SET_REGISTERED":
      return action.registered;
    default:
      return registered;
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

function userName(name = "", action) {
  switch (action.type) {
    case "USER_SET_NAME":
      return action.name;
    default:
      return name;
  }
}

function userClass(school_class = "", action) {
  switch (action.type) {
    case "USER_SET_CLASS":
      return action.school_class;
    default:
      return school_class;
  }
}

export default combineReducers({
  userEmail,
  userName,
  userClass,
  isAuthenticated,
  isRegistered,
});
