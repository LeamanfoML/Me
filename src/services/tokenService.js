const cron = require('node-cron');
const axios = require('axios');
const { autoTokenInterval, portalsApiUrl, tonnelApiUrl } = require('../config');
const logger = require('../utils/logger');

class TokenService {
  constructor() {
    this.portalsToken = null;
    this.tonnelToken = null;
    this.scheduleRefresh();
  }

  async refreshPortalsToken() {
    try {
      const res = await axios.post(`${portalsApiUrl}/auth/update_auth`);
      this.portalsToken = res.data.token;
      logger.info('Portals токен обновлён');
    } catch (err) {
      logger.error('Не удалось обновить Portals токен: %s', err.message);
    }
  }

  async refreshTonnelToken() {
    try {
      const res = await axios.post(`${tonnelApiUrl}/auth`);
      this.tonnelToken = res.data.token;
      logger.info('Tonnel токен обновлён');
    } catch (err) {
      logger.error('Не удалось обновить Tonnel токен: %s', err.message);
    }
  }

  scheduleRefresh() {
    // обновляем токены по расписанию
    cron.schedule(`*/${autoTokenInterval / 60} * * * *`, () => {
      this.refreshPortalsToken();
      this.refreshTonnelToken();
    });
  }
}

module.exports = new TokenService();
