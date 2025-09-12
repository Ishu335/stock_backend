from fastapi import FastAPI

app=FastAPI(
    prefix='/stock_backend'
    ,tags=['stock']
)

@app.post("/reward`")
async def add_reward():
    return {"message": "Reward added successfully"}

@app.get("/today-stocks/{userId}")
async def return_all_stock_user_today():
    return {"message": "Reward return successfully"}


@app.get("/histroical-inr/{userId}")
async def return_all_stock_user_today():
    return {"message": "Return the INR value of the user’s stock rewards for all past days (up to yesterday)."}

@app.get("/stats/{userId}")
async def return_status():
    return {"message": "- Total shares rewarded today (grouped by stock symbol)."
    "- Current INR value of the user’s portfolio. "}


@app.get("/portfolio/{userId}")
async def return_status():
    return {"message": "- Detailed holdings with current INR value"}



