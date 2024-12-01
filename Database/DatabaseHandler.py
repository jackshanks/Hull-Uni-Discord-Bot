import os

import aiosqlite
import random


class DatabaseHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseHandler, cls).__new__(cls)
            cls._instance.database_path = os.path.join(os.path.dirname(os.path.abspath("BotDB.db")),
                                                       "Database/BotDB.db")
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
            raise
        finally:
            await self._connection.close()

    async def get_default_rules(self):
        """Get the default rules."""
        try:
            await self.connect()
            async with await self._connection.execute("SELECT rule FROM rules") as cursor:
                rows = await cursor.fetchall()
                # Extract the 'rule' value from each Row object
                return [row['rule'] for row in rows]
        except Exception as e:
            print(f"Failed to get default rules: {str(e)}")
            raise
        finally:
            await self.close()

    async def get_quote(self):
        """Get a random quote."""
        try:
            await self.connect()
            return await self.execute_query("SELECT * FROM quotes ORDER BY RANDOM() LIMIT 1")
        except Exception as e:
            print(f"Get quote failed failed: {str(e)}")
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
            raise
        finally:
            await self.close()

    async def mark_quote_as_star(self, id):
        """Mark a quote as starred in the database."""
        try:
            await self.connect()
            async with self._connection.execute(
                    "UPDATE quotes SET star = 1 WHERE id = ?", (id,)
            ) as cursor:
                await self._connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Mark quote as star failed: {str(e)}")
            raise
        finally:
            await self.close()

    async def mark_quote_as_deleted(self, id):
        """Mark a quote as deleted in the database."""
        try:
            await self.connect()
            async with self._connection.execute("UPDATE quotes SET deleted = 1 WHERE id = ?", id) as cursor:
                await self._connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Mark quote as deleted failed: {str(e)}")
            raise
        finally:
            await self.close()

    async def get_quote_starred(self, id):
        try:
            await self.connect()
            result = await self.execute_query("SELECT star FROM quotes WHERE id = ?", id)
            if result == 0:
                return False
            elif result == 1:
                return True
            else:
                return None
        except Exception as e:
            print(f"Get quote star status failed: {str(e)}")
            raise
        finally:
            await self.close()

    async def submit_quote(self, id, content, said_by, quoted_by):
        """Submit a new quote to the database."""
        try:
            await self.connect()
            async with self._connection.execute(
                    """
                    INSERT INTO quotes (id, quote, said_by, quoted_by, deleted, star)
                    VALUES (?, ?, ?, ?, 0, 0)
                    """,
                    (id, content, said_by, quoted_by)
            ) as cursor:
                await self._connection.commit()
                return cursor.rowcount > 0
        except Exception as e:
            print(f"Submit quote failed: {str(e)}")
            raise
        finally:
            await self.close()
