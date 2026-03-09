from typing import Optional, List, Any

import peewee
import peewee_async
import pymysql
from peewee import __deprecated__
from peewee_async.utils import FetchResults
from playhouse.shortcuts import ReconnectMixin

# from psycopg2 import OperationalError, InterfaceError

from config.database import DB_CONFIG


class MysqlReconnectMixin(ReconnectMixin):
    def execute_sql(self, sql, params=None, commit=None):
        if commit is not None:
            __deprecated__('"commit" has been deprecated and is a no-op.')
        return self._reconnect(super(ReconnectMixin, self).execute_sql, sql, params)

    async def aio_reconnect(self, async_func, *args, **kwargs):
        try:
            return await async_func(*args, **kwargs)
        except Exception as exc:
            # If we are in a transaction, do not reconnect silently as
            # any changes could be lost.
            if self.in_transaction():
                raise exc

            exc_class = type(exc)
            if exc_class not in self._reconnect_errors:
                raise exc

            exc_repr = str(exc).lower()
            for err_fragment in self._reconnect_errors[exc_class]:
                if err_fragment in exc_repr:
                    break
            else:
                raise exc

            if not self.is_closed():
                self.close()
                self.connect()

            return await async_func(*args, **kwargs)

    async def aio_execute_sql(self, sql: str, params: Optional[List[Any]] = None, fetch_results: Optional[FetchResults] = None) -> Any:
        return await self.aio_reconnect(super(ReconnectMixin, self).aio_execute_sql, sql, params, fetch_results)


class ReconnectMySQLDatabase(MysqlReconnectMixin, peewee_async.PooledMySQLDatabase):
    reconnect_errors = (
        (peewee.OperationalError, "2006"),  # MySQL server has gone away.
        (peewee.OperationalError, "2003"),  # Can't connect to MySQL server on '***' ([Errno 111] Connection refused)
        (peewee.OperationalError, "2013"),  # Lost connection to MySQL server.
        (peewee.OperationalError, "2014"),  # Commands out of sync.
        (peewee.OperationalError, "4031"),  # Client interaction timeout.
        (peewee.OperationalError, "1053"),  # Server shutdown in progress
        (peewee.OperationalError, "1040"),
        (peewee.OperationalError, "1205"),  # 1205, 'Lock wait timeout exceeded; try restarting transaction'
        (peewee.OperationalError, "MySQL Connection not available."),
        (peewee.OperationalError, "terminat"),
        (peewee.OperationalError, "lost connection"),
        (peewee.InterfaceError, "connection already closed"),
        (pymysql.err.OperationalError, "2006"),  # MySQL server has gone away.
        (pymysql.err.OperationalError, "2003"),  # Can't connect to MySQL server on '***' ([Errno 111] Connection refused)
        (pymysql.err.OperationalError, "2013"),  # Lost connection to MySQL server.
        (pymysql.err.OperationalError, "2014"),  # Commands out of sync.
        (pymysql.err.OperationalError, "4031"),  # Client interaction timeout.
        (pymysql.err.OperationalError, "1053"),  # Server shutdown in progress
        (pymysql.err.OperationalError, "1040"),
        (pymysql.err.OperationalError, "1205"),  # 1205, 'Lock wait timeout exceeded; try restarting transaction'
        (pymysql.err.OperationalError, "MySQL Connection not available."),
        (pymysql.err.OperationalError, "terminat"),
        (pymysql.err.OperationalError, "lost connection"),
        (pymysql.err.InterfaceError, "connection already closed"),
    )


class PgReconnectMixin(ReconnectMixin):
    def execute_sql(self, sql, params=None, commit=None, named_cursor=None):
        return self._reconnect(super(ReconnectMixin, self).execute_sql, sql, params, named_cursor)

    async def aio_reconnect(self, async_func, *args, **kwargs):
        try:
            return await async_func(*args, **kwargs)
        except Exception as exc:
            # If we are in a transaction, do not reconnect silently as
            # any changes could be lost.
            if self.in_transaction():
                raise exc

            exc_class = type(exc)
            if exc_class not in self._reconnect_errors:
                raise exc

            exc_repr = str(exc).lower()
            for err_fragment in self._reconnect_errors[exc_class]:
                if err_fragment in exc_repr:
                    break
            else:
                raise exc

            if not self.is_closed():
                self.close()
                self.connect()

            return await async_func(*args, **kwargs)

    async def aio_execute_sql(self, sql: str, params: Optional[List[Any]] = None, fetch_results: Optional[FetchResults] = None) -> Any:
        return await self.aio_reconnect(super(ReconnectMixin, self).aio_execute_sql, sql, params, fetch_results)


class ReconnectPooledPostgresqlDatabase(PgReconnectMixin, peewee_async.PooledPostgresqlExtDatabase):
    reconnect_errors = (
        (peewee.OperationalError, "terminat"),
        (peewee.InterfaceError, "connection already closed"),
        (peewee.OperationalError, "eof detected"),
        (peewee.OperationalError, "remote datanode"),
        # Postgres error examples:
        # (OperationalError, "terminat"),
        # (InterfaceError, "connection already closed"),
        # (OperationalError, "eof detected"),
        # (OperationalError, "remote datanode"),
        # (FileNotFoundError, "no such file"),
    )


db = None

# Use MySQL configuration from DB_CONFIG
db = ReconnectMySQLDatabase(
    database=DB_CONFIG["database"],
    user=DB_CONFIG["user"],
    host=DB_CONFIG["host"],
    password=DB_CONFIG["password"],
    port=DB_CONFIG["port"],
    max_connections=10,
    # 设置东八区连接
    init_command="SET time_zone = '+08:00';",
)
db.set_allow_sync(True)
