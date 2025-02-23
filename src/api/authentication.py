from fastapi import APIRouter

authentication_router = APIRouter()

@authentication_router.post("/register/google")
async def register_google():
    pass

@authentication_router.post("/logout")
async def logout():
    pass

@authentication_router.post("/refresh")
async def refresh():
    pass

@authentication_router.get("/user-data")
async def get_user_data():
    pass