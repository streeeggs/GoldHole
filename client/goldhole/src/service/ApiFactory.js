const API_URL = process.env.API_URL;

export default class ApiFactory {
  constructor(route) {
    return fetch(API_URL + route);
  }
}
