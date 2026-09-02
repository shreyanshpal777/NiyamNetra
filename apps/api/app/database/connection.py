import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

_client: AsyncIOMotorClient | None = None
_db = None


class InMemoryCollection:
    def __init__(self):
        self.data = {}

    async def create_index(self, *args, **kwargs):
        pass

    async def insert_one(self, doc):
        doc_id = doc.get("_id") or doc.get("id")
        self.data[doc_id] = doc

    async def update_one(self, filter_dict, update_dict):
        doc_id = filter_dict.get("_id")
        if doc_id in self.data:
            if "$set" in update_dict:
                self.data[doc_id].update(update_dict["$set"])

    async def find_one(self, filter_dict, projection=None):
        doc_id = filter_dict.get("_id")
        doc = self.data.get(doc_id)
        if doc:
            return dict(doc)
        return None

    def find(self, filter_dict):
        class Cursor:
            def __init__(self, data_list):
                self.data_list = data_list
            def sort(self, *args, **kwargs):
                return self
            def skip(self, *args, **kwargs):
                return self
            def limit(self, *args, **kwargs):
                return self
            def __aiter__(self):
                self._iter = iter(self.data_list)
                return self
            async def __anext__(self):
                try:
                    return next(self._iter)
                except StopIteration:
                    raise StopAsyncIteration
        items = list(self.data.values())
        return Cursor(items)

    async def delete_one(self, filter_dict):
        doc_id = filter_dict.get("_id")
        if doc_id in self.data:
            del self.data[doc_id]
            class Result:
                deleted_count = 1
            return Result()
        class Result:
            deleted_count = 0
        return Result()


class InMemoryDB:
    def __init__(self):
        self.collections = {}

    def __getitem__(self, item):
        if item not in self.collections:
            self.collections[item] = InMemoryCollection()
        return self.collections[item]

    async def command(self, cmd):
        return {"ok": 1}


async def connect_to_mongo() -> None:
    global _client, _db
    settings = get_settings()
    try:
        _client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=2000)
        _db = _client[settings.mongodb_database]
        await _client.admin.command("ping")
        await _create_indexes()
    except Exception as e:
        logging.warning(f"MongoDB connection failed ({e}). Falling back to in-memory store.")
        _db = InMemoryDB()


async def _create_indexes() -> None:
    db = get_db()
    if isinstance(db, InMemoryDB):
        return
    await db["inspections"].create_index("status")
    await db["inspections"].create_index("created_at")
    await db["inspections"].create_index("product_name")
    await db["inspections"].create_index("category")


async def close_mongo_connection() -> None:
    global _client
    if _client:
        _client.close()


def get_db():
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_to_mongo() first.")
    return _db

