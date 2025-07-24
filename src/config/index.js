const dotenv = require('dotenv');
dotenv.config();

module.exports = {
  botToken: process.env.BOT_TOKEN,
  adminChatId: process.env.ADMINCHATID,
  portalsApiUrl: process.env.PORTALS_API_URL,
  tonnelApiUrl: process.env.TONNEL_API_URL,
  dbPath: process.env.DB_PATH,
  autoTokenInterval: Number(process.env.AUTO_TOKEN_INTERVAL),
  dataRefreshInterval: Number(process.env.DATA_REFRESH_INTERVAL),
  port: Number(process.env.PORT) || 3000
};
