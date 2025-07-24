const logger = require('./logger');

function errorHandler(err, req, res, next) {
  logger.error('Ошибка API: %s', err.message);
  res.status(500).json({ error: 'Внутренняя ошибка сервера' });
}

module.exports = errorHandler;
