from fastapi import FastAPI
from auth.api import auth_router
from users.api import user_router
from scan.api import scan_router
from fastapi.middleware.cors import CORSMiddleware
from admin.api import admin_router
from chat.api import chat_router


app = FastAPI(
    title="Skin Scan",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify your Flutter app's domain here instead of "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(scan_router.router)
app.include_router(admin_router.router)
app.include_router(chat_router.router)