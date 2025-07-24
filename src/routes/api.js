const express = require('express');
const { celebrate, Joi, errors } = require('celebrate');
const arbitrageCtrl = require('../controllers/arbitrageController');
const router = express.Router();

// Маршрут для обновления (вызов вручную или cron)
router.post('/update', arbitrageCtrl.updateData.bind(arbitrageCtrl));

// Маршрут получения данных с валидацией query
router.get(
  '/data',
  celebrate({
    query: Joi.object({
      minProfit: Joi.number().min(0).optional(),
      maxEndsAt: Joi.number().optional(),
      sortBy: Joi.string().valid('profit','time').optional()
    })
  }),
  arbitrageCtrl.getData.bind(arbitrageCtrl)
);

router.use(errors());

module.exports = router;
