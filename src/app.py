from fastapi import FastAPI
from src.api.authentication import authentication_router
from src.api.notes import notes_router
from src.core.database import db

def create_app() -> FastAPI:

    app = FastAPI()
    
    @app.on_event("startup")
    async def startup_db_client():
        await db.connect()


    BASE_API_PATH = "/api"
    V1_API_VERSION_PATH = BASE_API_PATH + "/v1"

    app.router.include_router(
        router=authentication_router,
        prefix=f"{V1_API_VERSION_PATH}/authentication",
        tags=["Authentication"]
    )

    app.router.include_router(
        router=notes_router,
        prefix=f"{V1_API_VERSION_PATH}/notes",
        tags=["Notes"]
    )
    
    @app.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    @app.on_event("shutdown")
    async def shutdown_db_client():
        await db.close()
    
    
    return app