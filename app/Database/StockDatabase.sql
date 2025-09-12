-- Drop in correct dependency order
DROP TABLE IF EXISTS ledger_entries;
DROP TABLE IF EXISTS ledger_transactions;
DROP TABLE IF EXISTS stock_price_history;
DROP TABLE IF EXISTS stock_prices;
DROP TABLE IF EXISTS rewards;
DROP TABLE IF EXISTS users;

-- Users
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name TEXT,
  email TEXT UNIQUE,
  password varchar(200) DEFAULT NULL, 
  is_active boolean DEFAULT NULL,
  created_at TIMESTAMP DEFAULT now()
  
);

-- Rewards
CREATE TABLE rewards (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id),
  stock_symbol TEXT NOT NULL,
  shares NUMERIC(18,6) NOT NULL,
  reward_ts TIMESTAMP NOT NULL,
  idempotency_key TEXT,
  created_at TIMESTAMP DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_rewards_idemp 
ON rewards(user_id, idempotency_key) 
WHERE idempotency_key IS NOT NULL;

-- Stock Prices (latest)
CREATE TABLE stock_prices (
  stock_symbol TEXT PRIMARY KEY,
  price_in_inr NUMERIC(18,4) NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

-- Stock Price History
CREATE TABLE stock_price_history (
  id SERIAL PRIMARY KEY,
  stock_symbol TEXT NOT NULL,
  price_in_inr NUMERIC(18,4) NOT NULL,
  captured_at TIMESTAMP NOT NULL
);

-- Ledger Transactions
CREATE TABLE ledger_transactions (
  id SERIAL PRIMARY KEY,
  tx_type TEXT,     -- e.g., 'purchase', 'distribution', 'fees', 'refund'
  reference_id INT, -- e.g., reward_id or purchase id
  created_at TIMESTAMP DEFAULT now()
);

-- Ledger Entries
CREATE TABLE ledger_entries (
  id SERIAL PRIMARY KEY,
  tx_id INT NOT NULL REFERENCES ledger_transactions(id),
  account TEXT NOT NULL,  -- e.g., 'ASSET:STOCK:RELIANCE', 'CASH:BANK'
  direction TEXT NOT NULL CHECK (direction IN ('debit','credit')),
  amount_in_inr NUMERIC(18,4) NOT NULL,
  shares NUMERIC(18,6),          -- optional for stock accounts
  stock_symbol TEXT,
  created_at TIMESTAMP DEFAULT now()
);
