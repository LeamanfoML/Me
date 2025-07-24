const express = require('express');
const cors = require('cors');
const apiRoutes = require('./routes/api');
const errorHandler = require('./utils/errorHandler');
const migrate = require('./models/migration');
const { port } = require('./config');
const logger = require('./utils/logger');
require('./services/tokenService'); // инициализация автообновления токенов

migrate(); // миграции SQLite

const app = express();
app.use(cors());
app.use(express.json());
app.use('/api', apiRoutes);
app.use(errorHandler);

app.use(express.static('public'));

app.listen(port, () => {
  logger.info(`Сервер запущен на порту ${port}`);
});
