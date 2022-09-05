import ApiFactory from "./ApiFactory";

export default class UserService {
  async getUsers() {
    let api = new ApiFactory("users");
    return await api.then((res) => res.json());
  }
  async getTopOffendersByTitle() {
    let api = new ApiFactory("users/top/title");
    return await api.then((res) => res.json());
  }
  async getTopOffendersByMessage() {
    let api = new ApiFactory("users/top/message");
    return await api.then((res) => res.json());
  }
  async getTopOffenderAndMessages() {
    let api = new ApiFactory("users/top/real");
    return await api.then((res) => res.json());
  }
}
