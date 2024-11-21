import os

import aiosqlite
import random


class DatabaseHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            cls._instance.database_path = os.path.join(os.path.dirname(os.path.abspath("BotDB.db")), "Database/BotDB.db")
            cls._instance._connection = None
        return cls._instance

    async def connect(self) -> None:
        """Initialize the database connection."""
        try:
            self._connection = await aiosqlite.connect(self.database_path)
            # Enable returning dictionaries instead of tuples for query results
            self._connection.row_factory = aiosqlite.Row
        except Exception as e:
            print(f"Failed to connect to database: {str(e)}")
            raise

    async def close(self) -> None:
        """Close the database connection."""
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def execute_query(self, query: str, *args):
        """Execute a database query."""

        if not self._connection:
            raise Exception("Database connection not initialized")

        await self.connect()

        try:
            async with await self._connection.execute(query, args) as cursor:
                row = await cursor.fetchone()
                return tuple(row) if row else None
        except Exception as e:
            print(f"Query execution failed: {str(e)}\nQuery: {query}")
            await self.close()
            raise
        finally:
            await self._connection.close()

    async def get_quote(self):
        """Get a random quote."""
        try:
            await self.connect()
            return await self.execute_query("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
        except Exception as e:
            print(f"Get quote failed failed: {str(e)}")
            await self.close()
            raise
        finally:
            await self.close()

    async def get_number_of_quotes(self):
        """Get number of quotes in the quote table."""
        try:
            await self.connect()
            result = await self.execute_query("SELECT COUNT(*) FROM quotes")
            return result[0]
        except Exception as e:
            print(f"Get number of quotes failed: {str(e)}")
            await self.close()
            raise
        finally:
            await self.close()

    async def mark_quote_as_star(self,id):
        pass
    
    async def mark_quote_as_deleted(self,id):
        pass

    async def get_quote_starred(self,id):
        pass

    async def submit_quote(self,id,content,said_by,quoted_by):
        pass