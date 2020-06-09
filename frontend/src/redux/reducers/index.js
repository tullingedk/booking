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

function user(
  user = { email: "", name: "", school_class: "", avatar: "", is_admin: false },
  action
) {
  switch (action.type) {
    case "USER_SET_EMAIL":
      return Object.assign({}, user, {
        email: action.email,
      });
    case "USER_SET_NAME":
      return Object.assign({}, user, {
        name: action.name,
      });
    case "USER_SET_CLASS":
      return Object.assign({}, user, {
        school_class: action.school_class,
      });
    case "USER_SET_AVATAR":
      return Object.assign({}, user, {
        avatar: action.avatar,
      });
    case "USER_IS_ADMIN":
      return Object.assign({}, user, {
        is_admin: action.is_admin,
      });
    default:
      return user;
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
  user,
  isAuthenticated,
  isRegistered,
  systemMeta,
});
