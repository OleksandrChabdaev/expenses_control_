const keyToken = "access_token";
export const getAccessToken = () => window.localStorage.getItem(keyToken);
export const setAccessToken = (token) =>
  window.localStorage.setItem(keyToken, token);
export const clearAccessToken = () => window.localStorage.removeItem(keyToken);
