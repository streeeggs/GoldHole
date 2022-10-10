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
  // Kill for now
  // async getTopOffenderAndMessages() {
  //   let api = new ApiFactory("users/top/real");
  //   return await api.then((res) => res.json());
  // }
  async getTopOffenderBinned(dateRange) {
    let api = new ApiFactory(`users/top/binned?date_bin=${dateRange}`);
    return await api.then((res) => res.json());
  }
  async getTopOffenders(dateRange = "ALLTIME", limit = 3) {
    let api = new ApiFactory(`users/top?date_bin=${dateRange}&limit=${limit}`);
    return await api.then((res) => res.json());
  }
}
