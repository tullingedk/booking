export function isAuthenticated(authenticated = false, action) {
  switch (action.type) {
    case "SET_AUTHENTICATED":
      return action.authenticated;
    default:
      return authenticated;
  }
}

export function isRegistered(registered = false, action) {
  switch (action.type) {
    case "SET_REGISTERED":
      return action.registered;
    default:
      return registered;
  }
}

export function user(
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

export function systemMeta(meta = { version: "", hash: "" }, action) {
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

export function event(
  event = { event_date: "", swish_name: "", swish_phone: "" },
  action
) {
  switch (action.type) {
    case "EVENT_SET_DATE":
      return Object.assign({}, event, {
        event_date: action.event_date,
      });
    case "EVENT_SET_SWISH_NAME":
      return Object.assign({}, event, {
        swish_name: action.swish_name,
      });
    case "EVENT_SET_SWISH_PHONE":
      return Object.assign({}, event, {
        swish_phone: action.swish_phone,
      });
    default:
      return event;
  }
}
