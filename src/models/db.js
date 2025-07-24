const sqlite3 = require('sqlite3').verbose();
const { dbPath } = require('../config');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Не удалось подключиться к SQLite:', err.message);
    process.exit(1);
  }
});

module.exports = db;
