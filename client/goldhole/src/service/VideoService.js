import ApiFactory from "./ApiFactory";

export default class VideoService {
  async getVideos() {
    let api = new ApiFactory("videos");
    return api.then((res) => res.json());
  }
  async getTopVideos() {
    let api = new ApiFactory("videos/top");
    return await api.then((res) => res.json());
  }
  async getHistory(name) {
    let api = new ApiFactory(`videos/history/${name}`);
    return await api.then((res) => res.json());
  }
}
