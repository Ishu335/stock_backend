

-- -- Drop in correct dependency order
DROP TABLE IF EXISTS ledger_entries CASCADE;
DROP TABLE IF EXISTS ledger_transactions CASCADE;
DROP TABLE IF EXISTS stock_price_history CASCADE;
DROP TABLE IF EXISTS stock_prices CASCADE;
DROP TABLE IF EXISTS rewards CASCADE;
DROP TABLE IF EXISTS portfolio CASCADE;
DROP TABLE IF EXISTS users CASCADE;

 -- TRUNCATE TABLE 
--   ledger_entries,
--   ledger_transactions,
--   stock_price_history,
--   stock_prices,
--   rewards,
--   portfolio,
--   users
-- RESTART IDENTITY CASCADE;


-- USERS TABLE
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR,
    email VARCHAR UNIQUE,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP NOT NULL,
    CONSTRAINT uq_users_email UNIQUE (email)
);

-- REWARDS TABLE
CREATE TABLE rewards (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id),
    stock_symbol VARCHAR NOT NULL,
    shares NUMERIC(18,6) NOT NULL,
    reward_ts TIMESTAMP NOT NULL,
    action_taken VARCHAR NOT NULL,
    share_price INT NOT NULL,
    total_price INT NOT NULL
);

-- STOCK PRICES TABLE
CREATE TABLE stock_prices (
    id INT,
    stock_symbol VARCHAR PRIMARY KEY,
    price_in_inr NUMERIC(18,4) NOT NULL,
    shares NUMERIC(18,6) NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    share_price INT NOT NULL,
    total_price INT NOT NULL
);

INSERT INTO stock_prices (id, stock_symbol, price_in_inr, shares, updated_at, share_price, total_price)
VALUES
  (1,  'TCS',        3850.75, 120, '2025-09-01 10:30:00', 3850, 462090),
  (2,  'INFY',       1525.40, 200, '2025-09-02 11:15:00', 1525, 305080),
  (3,  'RELIANCE',   2475.90, 300, '2025-09-03 09:45:00', 2475, 742770),
  (4,  'WIPRO',       445.60, 100, '2025-09-04 14:00:00', 445,   44560),
  (5,  'ITC',         452.30, 500, '2025-09-05 16:30:00', 452,  226150),
  (6,  'LT',         3685.75, 120, '2025-09-06 12:00:00', 3685, 442290),
  (7,  'SBIN',        735.20, 350, '2025-09-07 13:10:00', 735,  257320),
  (8,  'BAJFINANCE', 7200.00,  80, '2025-09-08 15:45:00', 7200, 576000),
  (9,  'AXISBANK',   1125.40, 210, '2025-09-09 11:25:00', 1125, 236334),
  (10, 'HCLTECH',    1755.60, 160, '2025-09-10 09:00:00', 1755, 280896),
  (11, 'ICICIBANK',   970.25, 400, '2025-09-11 10:20:00', 970,  388100),
  (12, 'SUNPHARMA',  1250.10, 140, '2025-09-12 14:40:00', 1250, 175014),
  (13, 'ONGC',        198.45, 600, '2025-09-13 12:10:00', 198,  119070),
  (14, 'ADANIPORTS', 1425.75, 250, '2025-09-14 17:30:00', 1425, 356438),
  (15, 'HDFCBANK',   1642.20, 150, '2025-09-15 09:15:00', 1642, 246330);


-- PORTFOLIO TABLE
CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    stock_symbol VARCHAR NOT NULL,
    shares NUMERIC NOT NULL,
    average_price NUMERIC(18,2),
    current_price NUMERIC(18,2),
    total_value NUMERIC(18,2),
    last_updated TIMESTAMP
);

-- STOCK PRICE HISTORY TABLE
CREATE TABLE stock_price_history (
    id SERIAL PRIMARY KEY,
    stock_symbol VARCHAR NOT NULL,
    average_price NUMERIC(18,4) NOT NULL,
    current_price NUMERIC(18,4) NOT NULL,
    shares NUMERIC(18,4) NOT NULL,
    total_price NUMERIC(18,4) NOT NULL,
    captured_at TIMESTAMP NOT NULL
);
INSERT INTO stock_price_history 
(stock_symbol, average_price, current_price, shares, total_price, captured_at)
VALUES
  -- TCS
  ('TCS', 3800.50, 3850.75, 120, 462090.00, '2025-09-10 10:30:00'),
  ('TCS', 3825.00, 3900.25, 120, 468030.00, '2025-09-11 10:30:00'),
  ('TCS', 3850.00, 3925.00, 120, 471000.00, '2025-09-12 10:30:00'),

  -- INFY
  ('INFY', 1500.25, 1525.40, 200, 305080.00, '2025-09-10 11:00:00'),
  ('INFY', 1512.00, 1535.10, 200, 307020.00, '2025-09-11 11:00:00'),
  ('INFY', 1520.00, 1540.50, 200, 308100.00, '2025-09-12 11:00:00'),

  -- RELIANCE
  ('RELIANCE', 2450.60, 2475.90, 300, 742770.00, '2025-09-10 09:45:00'),
  ('RELIANCE', 2465.00, 2490.30, 300, 747090.00, '2025-09-11 09:45:00'),
  ('RELIANCE', 2480.00, 2505.50, 300, 751650.00, '2025-09-12 09:45:00'),

  -- HDFCBANK
  ('HDFCBANK', 1625.50, 1642.20, 150, 246330.00, '2025-09-10 14:20:00'),
  ('HDFCBANK', 1638.00, 1655.50, 150, 248325.00, '2025-09-11 14:20:00'),
  ('HDFCBANK', 1645.00, 1662.80, 150, 249420.00, '2025-09-12 14:20:00'),

  -- SBIN
  ('SBIN', 725.10, 735.20, 350, 257320.00, '2025-09-10 16:00:00'),
  ('SBIN', 730.00, 745.00, 350, 260750.00, '2025-09-11 16:00:00'),
  ('SBIN', 740.00, 755.20, 350, 264320.00, '2025-09-12 16:00:00');
INSERT INTO stock_price_history 
(stock_symbol, average_price, current_price, shares, total_price, captured_at)
VALUES
  -- WIPRO
  ('WIPRO', 440.00, 445.60, 100, 44560.00, '2025-09-10 15:00:00'),
  ('WIPRO', 442.00, 448.25, 100, 44825.00, '2025-09-11 15:00:00'),
  ('WIPRO', 445.00, 450.00, 100, 45000.00, '2025-09-12 15:00:00'),

  -- ITC
  ('ITC', 448.50, 452.30, 500, 226150.00, '2025-09-10 13:45:00'),
  ('ITC', 450.00, 455.00, 500, 227500.00, '2025-09-11 13:45:00'),
  ('ITC', 452.00, 457.50, 500, 228750.00, '2025-09-12 13:45:00'),

  -- BAJFINANCE
  ('BAJFINANCE', 7150.00, 7200.00, 80, 576000.00, '2025-09-10 12:00:00'),
  ('BAJFINANCE', 7180.00, 7250.00, 80, 580000.00, '2025-09-11 12:00:00'),
  ('BAJFINANCE', 7200.00, 7280.00, 80, 582400.00, '2025-09-12 12:00:00'),

  -- HCLTECH
  ('HCLTECH', 1740.00, 1755.60, 160, 280896.00, '2025-09-10 10:15:00'),
  ('HCLTECH', 1750.00, 1765.40, 160, 282464.00, '2025-09-11 10:15:00'),
  ('HCLTECH', 1760.00, 1770.00, 160, 283200.00, '2025-09-12 10:15:00'),

  -- ADANIPORTS
  ('ADANIPORTS', 1410.00, 1425.75, 250, 356438.00, '2025-09-10 17:00:00'),
  ('ADANIPORTS', 1420.00, 1438.50, 250, 359625.00, '2025-09-11 17:00:00'),
  ('ADANIPORTS', 1430.00, 1445.20, 250, 361300.00, '2025-09-12 17:00:00');

-- LEDGER TRANSACTIONS TABLE
CREATE TABLE ledger_transactions (
    id SERIAL PRIMARY KEY,
    tx_type VARCHAR NOT NULL,
    reference_id INT,
    created_at TIMESTAMP
);

-- LEDGER ENTRIES TABLE
CREATE TABLE ledger_entries (
    id SERIAL PRIMARY KEY,
    tx_id INT NOT NULL REFERENCES ledger_transactions(id),
    account VARCHAR NOT NULL,
    direction VARCHAR NOT NULL,
    amount_in_inr NUMERIC(18,4) NOT NULL,
    shares NUMERIC(18,6),
    stock_symbol VARCHAR,
    created_at TIMESTAMP
);

















