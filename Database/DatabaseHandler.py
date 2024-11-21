import os

import aiosqlite
import random


class DatabaseHandler:
    def __init__(self):
        self.database_path = os.path.join(os.path.dirname(os.path.abspath("BotDB.db")), "Database\BotDB.db")
        self._connection: aiosqlite.Connection = None

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

        try:
            async with await self._connection.execute(query, args) as cursor:
                row = await cursor.fetchone()
                return tuple(row) if row else None
        except Exception as e:
            print(f"Query execution failed: {str(e)}\nQuery: {query}")
            raise

    async def get_quote(self):
        """Get a random quote."""
        return await self.execute_query("SELECT * FROM quotes ORDER BY RAND() LIMIT 1")

    async def get_number_of_quotes(self):
        """Get number of quotes in the quote table."""
        result = await self.execute_query("SELECT COUNT(*) FROM quotes")
        return result[0]

    async def mark_quote_as_star(self,id):
        pass
    
    async def mark_quote_as_deleted(self,id):
        pass

    async def get_quote_starred(self,id):
        pass