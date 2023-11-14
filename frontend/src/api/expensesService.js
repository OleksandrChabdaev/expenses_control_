import api from "./webApiHelper";

export const updateUser = async (id, data) => {
  return api.patch(`/api/user/${id}/`, data);
};

export const getAllExpenses = async () => {
  return api.get("/api/expenses/");
};

export const getFilterExpenses = async (data) => {
  return api.get("/api/expenses/", data);
};
export const creatExpenses = async (data) => {
  return api.post("/api/expenses/", data);
};

export const updateExpenses = async (id, data) => {
  return api.patch(`/api/expenses/${id}/`, data);
};

export const deleteExpenses = async (id) => {
  return api.delete(`/api/expenses/${id}/`);
};

export const login = async (token) => {
  return api.login_post(`/api/google/`, { access_token: token });
};

export const logout = async () => {
  return api.post(`/api/logout/`);
};
