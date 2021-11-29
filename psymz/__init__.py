"""
PsyMz

A simple python package for keeping Postgres connections alive indefinitely.
"""

__version__ = "1.0.0"
__author__ = 'John Ades'
__credits__ = 'https://www.psycopg.org/'

import psycopg2


class PostgresConnection:
    conn = None

    def __init__(self, **kwargs):
        self.creds = {}
        if "host" in kwargs:
            self.creds["host"] = kwargs["host"]
        if "port" in kwargs:
            self.creds["port"] = kwargs["port"]
        if "db" in kwargs:
            self.creds["dbname"] = kwargs["db"]
        if "user" in kwargs:
            self.creds["user"] = kwargs["user"]
        if "password" in kwargs:
            self.creds["password"] = kwargs["password"]
        # get keys from aws secrets manager
        self.connect()

    def __connected(self) -> bool:
        return self.conn and self.conn.closed == 0

    def connect(self):
        self.close()
        self.conn = psycopg2.connect(**self.creds)

    def close(self):
        if self.__connected():
            # noinspection PyBroadException
            try:
                self.conn.close()
            except Exception:
                pass
        self.conn = None

    def execute(self, statement, args=None, return_result=True, fetchone=False):
        return self.__execute__(
            statement=statement,
            args=args,
            return_result=return_result,
            fetchone=fetchone,
            allow_reconnect=True
        )

    def __execute__(self, statement, args, return_result, fetchone, allow_reconnect=True):
        try:
            with self.conn.cursor() as cur:
                if args is None:
                    cur.execute(statement)
                else:
                    cur.execute(statement, args)
                self.conn.commit()

                if return_result is True and fetchone is False:
                    result = cur.fetchall()
                    cur.close()
                    return result

                elif return_result is True and fetchone is True:
                    result = cur.fetchone()
                    cur.close()
                    return result
                else:
                    cur.close()

        except (psycopg2.OperationalError, psycopg2.DatabaseError) as e:
            if allow_reconnect is False:
                self.conn.rollback()
                if cur is not None:
                    cur.close()
                raise e
            # reconnect and retry
            self.connect()
            return self.__execute__(statement, args, return_result, fetchone, allow_reconnect=False)

        except Exception as e:
            self.conn.rollback()
            raise e

    def execute_many(self, size: int, statement: str, args=None):
        self.__execute_many__(size=size, statement=statement, args=args, allow_reconnect=True)

    def __execute_many__(self, size: int, statement: str, args=None, allow_reconnect=True):
        try:
            with self.conn.cursor() as cur:
                if args is None:
                    cur.execute(statement)
                else:
                    cur.execute(statement, args)
                self.conn.commit()

                while True:
                    # consume result over a series of iterations
                    # with each iteration fetching 2000 records
                    records = cur.fetchmany(size=size)
                    if not records:
                        break
                    for r in records:
                        yield r
        except (psycopg2.OperationalError, psycopg2.DatabaseError) as e:
            if allow_reconnect is False:
                self.conn.rollback()
                if cur is not None:
                    cur.close()
                raise e
            # reconnect and retry
            self.connect()
            self.__execute_many__(size=size, statement=statement, args=args, allow_reconnect=allow_reconnect)

        except Exception as e:
            self.conn.rollback()
            raise e

        finally:
            if cur is not None:
                cur.close()
