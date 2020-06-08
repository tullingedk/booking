import { USER_SET_EMAIL } from "./actionTypes";

export const setUserEmail = (email) => ({
  type: USER_SET_EMAIL,
  email,
});

export const setAuthenticated = (authenticated) => ({
  type: SET_AUTHENTICATED,
  authenticated,
});
