from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings

class Database:
    client: AsyncIOMotorClient = None
    
    def get_database(self):
        return self.client[settings.mongodb_db_name]

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.mongodb_url)
        await self.client.admin.command('ping')
        print("Connected to MongoDB")

    async def close(self):
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# Create a global instance
db = Database()