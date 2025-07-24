const db = require('./db');
const logger = require('../utils/logger');

async function migrate() {
  db.serialize(() => {
    db.run(`
      CREATE TABLE IF NOT EXISTS auctions (
        id TEXT PRIMARY KEY,
        name TEXT,
        model TEXT,
        ends_at INTEGER,
        current_bid REAL,
        portals_price REAL,
        tonnel_price REAL,
        profit REAL,
        last_updated INTEGER
      );
    `);
    logger.info('Миграции выполнены успешно');
  });
}

if (require.main === module) {
  migrate();
}

module.exports = migrate;
