const keyUser = "active_user";
export const getActiveUser = () =>
  JSON.parse(window.localStorage.getItem(keyUser));
export const setActiveUser = (userData) =>
  window.localStorage.setItem(keyUser, JSON.stringify(userData));
export const updateActiveUser = (userData) => {
  const user = JSON.parse(window.localStorage.getItem(keyUser));
  const user_new = Object.assign(user, userData);
  console.log(userData)
  setActiveUser(user_new);
  return user_new;
};
export const clearActiveUser = () => window.localStorage.removeItem(keyUser);
