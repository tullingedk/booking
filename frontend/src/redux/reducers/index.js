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

function userAvatar(avatar = "", action) {
  switch (action.type) {
    case "USER_SET_AVATAR":
      return action.avatar;
    default:
      return avatar;
  }
}

function systemMeta(meta = { version: "", hash: "" }, action) {
  switch (action.type) {
    case "SYSTEM_SET_VERSION":
      return Object.assign({}, meta, {
        version: action.version,
      });
    case "SYSTEM_SET_HASH":
      return Object.assign({}, meta, {
        hash: action.hash,
      });
    default:
      return meta;
  }
}

export default combineReducers({
  userEmail,
  userName,
  userClass,
  userAvatar,
  isAuthenticated,
  isRegistered,
  systemMeta,
});
