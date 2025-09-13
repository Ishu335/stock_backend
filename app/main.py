from fastapi import FastAPI
from routers import user,admin,share_market,task

app=FastAPI()   

app.include_router(admin.router)
app.include_router(user.router)
app.include_router(task.router)
app.include_router(share_market.router)

