import axios from "axios";
import { getAccessToken } from "../helpers/accessToken.helper";

const BASE_URL = process.env.REACT_APP_API_URL || window.location.origin;

class Api {
  baseUrl;
  instance;
  constructor() {
    this.baseUrl = BASE_URL;
    this.instance = axios.create({
      baseURL: BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
    });
  }

  async get(url, params) {
    return await this.instance
      .get(url, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
        params,
      })
      .then(this.handleResponse)
      .catch(this.handleError);
  }

  async post(url, data) {
    return await this.instance
      .post(url, data, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
      })
      .then(this.handleResponse)
      .catch(this.handleError);
  }

  async login_post(url, data) {
    return await this.instance
      .post(url, data, {})
      .then(this.handleResponse)
      .catch(this.handleError);
  }

  async patch(url, data) {
    return await this.instance
      .patch(url, data, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
      })
      .then(this.handleResponse)
      .catch(this.handleError);
  }

  async delete(url, data) {
    return await this.instance
      .delete(url, {
        headers: {
          Authorization: `Bearer ${getAccessToken()}`,
        },
        data,
      })
      .then(this.handleResponse)
      .catch(this.handleError);
  }

  handleResponse(response) {
    return response.data;
  }

  handleError(error) {
    if (error.response) {
      const data = error.response?.data;
      const message = Object.values(data).flat().join(" ");
      return { error: { data, message } };
    } else {
      return { error: { data: {}, message: error?.message } };
    }
  }
}

export default new Api();
