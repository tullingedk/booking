import {
  USER_SET_EMAIL,
  USER_SET_NAME,
  USER_SET_CLASS,
  USER_SET_AVATAR,
  SET_AUTHENTICATED,
  SET_REGISTERED,
  SYSTEM_SET_VERSION,
  SYSTEM_SET_HASH,
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
