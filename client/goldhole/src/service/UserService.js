import ApiFactory from "./ApiFactory";

export default class UserService {
  async getTopOffendersByTitle() {
    let api = new ApiFactory("users/top/title");
    return await api.then((res) => res.json());
  }
  async getTopOffendersByMessage() {
    let api = new ApiFactory("users/top/message");
    return await api.then((res) => res.json());
  }
  async getTopOffenderBinned(dateRange) {
    let api = new ApiFactory(`users?date_bin=${dateRange}&limit=3`);
    return await api.then((res) => res.json());
  }
  async getOffenderCount(dateRange) {
    let api = new ApiFactory(`users/top?date_bin=${dateRange}`);
    return await api.then((res) => res.json());
  }
}
