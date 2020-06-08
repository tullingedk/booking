import {
  USER_SET_EMAIL,
  USER_SET_NAME,
  USER_SET_CLASS,
  SET_AUTHENTICATED,
  SET_REGISTERED,
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

export const setAuthenticated = (authenticated) => ({
  type: SET_AUTHENTICATED,
  authenticated,
});

export const setRegistered = (registered) => ({
  type: SET_REGISTERED,
  registered,
});
