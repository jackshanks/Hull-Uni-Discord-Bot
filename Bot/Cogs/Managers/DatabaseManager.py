import os
import aiosqlite
import oracledb
from oracledb import Cursor


class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance.dns = "(description= (retry_count=10)(retry_delay=3)(address=(protocol=tcps)(port=1522)(host=adb.uk-london-1.oraclecloud.com))(connect_data=(service_name=g7701e72ed4f49e_r7x0dlybxyug7n1z_low.adb.oraclecloud.com))(security=(ssl_server_dn_match=yes)))"
            cls._instance._connection = None
        return cls._instance

    async def connect(self) -> None:
        """Initialize the database connection."""
        self._connection = (await oracledb.connect_async
                            (user="admin",
                             password="1",
                             dsn=self.dns))

    async def close(self):
        """Close the database connection."""
        if self._connection is not None:
            await self._connection.close()
            self._connection = None

    async def execute(self, query: str, params: tuple = None) -> tuple:
        """Execute a query and return the results."""
        if not self._connection:
            await self.connect()

        try:
            cursor = self._connection.cursor()
            await cursor.execute(query, params)
            if not query.__contains__("INSERT"):
                result = await cursor.fetchall()
                return result
            else:
                await self._connection.commit()

        except Exception as e:
            raise e

        finally:
            await self.close()
