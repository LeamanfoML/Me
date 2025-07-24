const axios = require('axios');
const { tonnelApiUrl } = require('../config');
const logger = require('../utils/logger');

class TonnelService {
  async fetchGifts() {
    try {
      const res = await axios.get(`${tonnelApiUrl}/auctions`);
      return res.data.gifts; // массив лотов
    } catch (err) {
      logger.error('Ошибка Tonnel API: %s', err.message);
      throw err;
    }
  }
}

module.exports = new TonnelService();
