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
  name  varchar(20),
  email  varchar(25) UNIQUE,
  password varchar(200) DEFAULT NULL, 
  created_at TIMESTAMP DEFAULT now() 
);

-- Rewards
CREATE TABLE rewards (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL,
  stock_symbol TEXT NOT NULL,
  shares NUMERIC NOT NULL,
  reward_ts TIMESTAMP NOT NULL,
  action_taken TEXT,
  share_price NUMERIC(18,2),                   
  total_price NUMERIC(18,2)
);


-- Stock Prices (latest)
CREATE TABLE stock_prices(
  id SERIAL ,
  stock_symbol TEXT PRIMARY KEY,
  shares BIGINT ,
  price_in_inr NUMERIC(18,2) NOT NULL,
  updated_at TIMESTAMP NOT NULL
);

CREATE TABLE portfolio (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    stock_symbol TEXT NOT NULL,
    shares NUMERIC NOT NULL,
    average_price NUMERIC(18,2),
    current_price NUMERIC(18,2),
    total_value NUMERIC(18,2) ,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
