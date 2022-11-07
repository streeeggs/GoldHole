import ApiFactory from "./ApiFactory";

export default class MessageService {
  async getMessages() {
    let api = new ApiFactory("messages/list");
    return await api.then((res) => res.json());
  }
}
