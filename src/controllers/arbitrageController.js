const portalsService = require('../services/portalsService');
const tonnelService = require('../services/tonnelService');
const db = require('../models/db');
const logger = require('../utils/logger');

// Комиссии и constants
const PORTALS_FEE = 0.05;
const TONNEL_FEE = 0.06;
const TRANSFER_FEE = 0.22;

class ArbitrageController {
  // Получить и сохранить арбитражные позиции
  async updateData(req, res, next) {
    try {
      const [portalsAuctions, tonnelGifts] = await Promise.all([
        portalsService.fetchAuctions(),
        tonnelService.fetchGifts()
      ]);

      const timestamp = Date.now();
      const stmt = db.prepare(`
        INSERT OR REPLACE INTO auctions
        (id, name, model, ends_at, current_bid, portals_price, tonnel_price, profit, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      `);

      portalsAuctions.forEach(a => {
        const pPrice = a.currentBid * (1 + PORTALS_FEE);
        const tMatch = tonnelGifts.find(g => g.id === a.id);
        if (!tMatch) return;
        const tPrice = tMatch.price * (1 - TONNEL_FEE) - TRANSFER_FEE;
        const profit = tPrice - pPrice;
        if (profit <= 0.1) return;

        stmt.run(
          a.id,
          a.name,
          a.model,
          new Date(a.endsAt).getTime(),
          a.currentBid,
          pPrice,
          tPrice,
          profit,
          timestamp
        );
      });

      stmt.finalize();
      return res.json({ success: true });
    } catch (err) {
      next(err);
    }
  }

  // Выдать данные клиенту
  async getData(req, res, next) {
    try {
      const { minProfit, maxEndsAt, sortBy } = req.query;
      let query = 'SELECT * FROM auctions WHERE profit > 0.1';
      const params = [];

      if (minProfit) {
        query += ' AND profit >= ?';
        params.push(Number(minProfit));
      }
      if (maxEndsAt) {
        query += ' AND ends_at <= ?';
        params.push(Number(maxEndsAt));
      }
      if (sortBy === 'profit') {
        query += ' ORDER BY profit DESC';
      } else {
        query += ' ORDER BY ends_at ASC';
      }

      db.all(query, params, (err, rows) => {
        if (err) return next(err);
        res.json(rows);
      });
    } catch (err) {
      next(err);
    }
  }
}

module.exports = new ArbitrageController();
