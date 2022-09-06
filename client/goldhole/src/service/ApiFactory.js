export default class ApiFactory {
  constructor(route) {
    return fetch(process.env.VUE_APP_API_URL + route);
  }
}
