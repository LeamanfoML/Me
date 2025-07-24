const axios = require('axios');
const { portalsApiUrl } = require('../config');
const logger = require('../utils/logger');

class PortalsService {
  async fetchAuctions() {
    try {
      const res = await axios.get(`${portalsApiUrl}/auctions`);
      return res.data.auctions; // массив аукционов
    } catch (err) {
      logger.error('Ошибка Portals API: %s', err.message);
      throw err;
    }
  }
}

module.exports = new PortalsService();
