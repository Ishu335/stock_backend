# Stocky Backend

A backend service for **Stocky**, a platform where users earn shares of Indian stocks (e.g., Reliance, TCS, Infosys) as rewards.  
Built with **FastAPI** and **SQLAlchemy**.

---

## Features
- Reward users with stock shares.
- View today’s rewarded stocks.
- Track historical INR values of rewards.
- Get portfolio statistics and current valuation.
- Mock service for stock price updates.

---

## API Endpoints

- **POST /reward** → Record rewarded shares for a user.  
- **GET /today-stocks/{userId}** → Get today’s rewards.  
- **GET /historical-inr/{userId}** → Get historical INR values.  
- **GET /stats/{userId}** → Get today’s shares and total portfolio value.  
- *(Bonus)* **GET /portfolio/{userId}** → Show holdings grouped by stock.

---

## Tech Stack
- FastAPI (framework)  
- SQLAlchemy (ORM)  
- SQLite/PostgreSQL (database)  
- Pydantic (data validation)

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/Ishu335/stock_backend.git
cd stock_backend

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
