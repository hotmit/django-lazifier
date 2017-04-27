from abc import ABCMeta, abstractmethod
from django.conf import settings


class DbBackend:
    MYSQL = 'django.db.backends.mysql'
    MSSQL = 'sqlserver_ado'
    POSTGRESQL = 'postgresql'


class DbNormBase:
    __metaclass__ = ABCMeta

    def __init__(self, backend, using='default'):
        self.using = using
        self.backend = backend

    @abstractmethod
    def is_null(self, field_name):
        """
        Check if a field is null.
        eg. is_null('zone')     => mysql returns 'zone is NULL', mssql returns 'ISNULL(zone)'

        :param field_name:
        :return:
        """
        pass

    @abstractmethod
    def to_unix_timestamp(self, field_name):
        """
        Convert timestamp into unix_timestamp/epoch time.

        :param field_name:
        :return:
        """
        pass

    @abstractmethod
    def limit(self, offset, row_count):
        """
        Limit the number of rows return from the query.

        :param offset: offset index
        :param row_count: number of rows to get
        :return: the limit string for each backend
        """
        pass


class DbNormMySql(DbNormBase):
    @classmethod
    def is_db_engine(cls, backend_engine):
        return backend_engine == DbBackend.MYSQL

    def __init__(self, using='default'):
        super().__init__(backend=DbBackend.MYSQL, using=using)

    def is_null(self, field_name):
        return '`%s` IS NULL' % field_name

    def to_unix_timestamp(self, field_name):
        return 'UNIX_TIMESTAMP(`%s`)' % field_name

    def limit(self, offset, row_count):
        return 'LIMIT %s, %s' % (offset, row_count)


class DbNormPostgreSql(DbNormBase):

    @classmethod
    def is_db_engine(cls, backend_engine):
        if DbBackend.POSTGRESQL in backend_engine:
            return True
        if 'postgis' in backend_engine:
            return True

        return False

    def __init__(self, using='default'):
        super().__init__(backend=DbBackend.POSTGRESQL, using=using)

    def is_null(self, field_name):
        return '"%s" IS NULL' % field_name

    def to_unix_timestamp(self, field_name):
        # double to escape literal
        return 'EXTRACT(EPOCH FROM "%s")' % field_name

    def limit(self, offset, row_count):
        return 'LIMIT %s OFFSET %s' % (row_count, offset)


class DbNormMsSql(DbNormBase):
    @classmethod
    def is_db_engine(cls, backend_engine):
        return backend_engine == DbBackend.MSSQL

    def __init__(self, using='default'):
        super().__init__(backend=DbBackend.MSSQL, using=using)

    def is_null(self, field_name):
        return 'CASE WHEN (%s IS NULL) THEN 1 ELSE 0 END' % field_name

    def to_unix_timestamp(self, field_name):
        return "CAST(DATEDIFF(SECOND,{d '1970-01-01'}, [%s]) AS BIGINT)" % field_name

    def limit(self, offset, row_count):
        return 'OFFSET %s ROWS FETCH NEXT %s ROWS ONLY' % (offset, row_count)


class DbNorm:
    @classmethod
    def get_backend_engine(cls, using='default'):
        engine = settings.DATABASES[using]['ENGINE']

        if engine == DbBackend.MYSQL or engine == DbBackend.MSSQL:
            return engine
        if DbNormPostgreSql.is_db_engine(engine):
            return DbBackend.POSTGRESQL

    @classmethod
    def get_db_normalizer(cls, using='default'):
        engine = DbNorm.get_backend_engine(using)

        if engine == DbBackend.MYSQL:
            return DbNormMySql(using)
        elif DbNormPostgreSql.is_db_engine(engine):
            return DbNormPostgreSql(using)
        elif engine == DbBackend.MSSQL:
            return DbNormMsSql(using)
        else:
            raise Exception('Db Normalization only supports MySQL, PostgreSQL and MSSQL.')
