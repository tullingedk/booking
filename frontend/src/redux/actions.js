import {
  USER_SET_EMAIL,
  USER_SET_NAME,
  USER_SET_CLASS,
  USER_SET_AVATAR,
  USER_IS_ADMIN,
  SET_AUTHENTICATED,
  SET_REGISTERED,
  SYSTEM_SET_VERSION,
  SYSTEM_SET_HASH,
  EVENT_SET_DATE,
  EVENT_SET_SWISH_NAME,
  EVENT_SET_SWISH_PHONE,
} from "./actionTypes";

export const setUserEmail = (email) => ({
  type: USER_SET_EMAIL,
  email,
});

export const setUserName = (name) => ({
  type: USER_SET_NAME,
  name,
});

export const setUserClass = (school_class) => ({
  type: USER_SET_CLASS,
  school_class,
});

export const setUserAvatar = (avatar) => ({
  type: USER_SET_AVATAR,
  avatar,
});

export const setIsAdmin = (is_admin) => ({
  type: USER_IS_ADMIN,
  is_admin,
});

export const setAuthenticated = (authenticated) => ({
  type: SET_AUTHENTICATED,
  authenticated,
});

export const setRegistered = (registered) => ({
  type: SET_REGISTERED,
  registered,
});

export const setVersion = (version) => ({
  type: SYSTEM_SET_VERSION,
  version,
});

export const setHash = (hash) => ({
  type: SYSTEM_SET_HASH,
  hash,
});

export const setEventDate = (event_date) => ({
  type: EVENT_SET_DATE,
  event_date,
});

export const setEventSwishName = (swish_name) => ({
  type: EVENT_SET_SWISH_NAME,
  swish_name,
});

export const setEventSwishPhone = (swish_phone) => ({
  type: EVENT_SET_SWISH_PHONE,
  swish_phone,
});
