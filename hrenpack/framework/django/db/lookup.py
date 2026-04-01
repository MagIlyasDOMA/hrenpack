from django.db import models
from django.db.models import Func, Lookup
from django.db.models.fields import CharField


class Dirname(Func):
    """
    Выражение для получения директории из пути к файлу
    Поддерживает Windows и Unix пути
    """
    function = None  # Будет переопределено в зависимости от БД
    arity = 1
    output_field = CharField()

    def __init__(self, expression, **extra):
        super().__init__(expression, **extra)
        self._db_type = None

    def as_sqlite(self, compiler, connection, **extra_context):
        # SQLite: используем встроенную функцию для работы с путями
        return self._get_sqlite_sql(compiler, connection, **extra_context)

    def as_postgresql(self, compiler, connection, **extra_context):
        # PostgreSQL: используем regexp_replace
        return self._get_postgresql_sql(compiler, connection, **extra_context)

    def as_mysql(self, compiler, connection, **extra_context):
        # MySQL: используем SUBSTRING_INDEX
        return self._get_mysql_sql(compiler, connection, **extra_context)

    def as_oracle(self, compiler, connection, **extra_context):
        # Oracle: используем REGEXP_SUBSTR
        return self._get_oracle_sql(compiler, connection, **extra_context)

    def as_sql(self, compiler, connection, **extra_context):
        # Дефолтная реализация для неподдерживаемых БД
        return self._get_fallback_sql(compiler, connection, **extra_context)

    def _get_sqlite_sql(self, compiler, connection, **extra_context):
        # SQLite не имеет встроенной функции для извлечения директории
        # Используем комбинацию substr и instr
        path, path_params = compiler.compile(self.source_expressions[0])

        # SQLite: извлекаем всё до последнего '/' или '\'
        # Используем CASE для обработки разных типов путей
        sql = """
            CASE 
                WHEN INSTR(%s, '/') > 0 AND INSTR(%s, '\\') > 0 THEN
                    CASE 
                        WHEN INSTR(%s, '/') > INSTR(%s, '\\') 
                        THEN SUBSTR(%s, 1, INSTR(%s, '/') - 1)
                        ELSE SUBSTR(%s, 1, INSTR(%s, '\\') - 1)
                    END
                WHEN INSTR(%s, '/') > 0 THEN SUBSTR(%s, 1, INSTR(%s, '/') - 1)
                WHEN INSTR(%s, '\\') > 0 THEN SUBSTR(%s, 1, INSTR(%s, '\\') - 1)
                ELSE %s
            END
        """ % tuple([path] * 15)

        return sql, path_params * 12

    def _get_postgresql_sql(self, compiler, connection, **extra_context):
        path, path_params = compiler.compile(self.source_expressions[0])

        # PostgreSQL: используем regexp_replace
        sql = """
            REGEXP_REPLACE(
                %s, 
                '[\\/\\\\][^\\/\\\\]+$', 
                ''
            )
        """ % path

        return sql, path_params

    def _get_mysql_sql(self, compiler, connection, **extra_context):
        path, path_params = compiler.compile(self.source_expressions[0])

        # MySQL: используем SUBSTRING_INDEX с обработкой Windows и Unix
        sql = """
            IF(
                LOCATE('/', %s) > 0 OR LOCATE('\\', %s) > 0,
                SUBSTRING_INDEX(
                    SUBSTRING_INDEX(
                        REPLACE(%s, '\\', '/'), 
                        '/', 
                        LENGTH(REPLACE(%s, '\\', '/')) - 
                        LENGTH(REPLACE(REPLACE(%s, '\\', '/'), '/', ''))
                    ),
                    '/',
                    -1
                ),
                %s
            )
        """ % tuple([path] * 6)

        return sql, path_params * 6

    def _get_oracle_sql(self, compiler, connection, **extra_context):
        path, path_params = compiler.compile(self.source_expressions[0])

        # Oracle: используем REGEXP_SUBSTR
        sql = """
            REGEXP_SUBSTR(%s, '^.*[\\/\\\\]', 1, 1)
        """ % path

        return sql, path_params

    def _get_fallback_sql(self, compiler, connection, **extra_context):
        # Дефолтная реализация для других БД
        path, path_params = compiler.compile(self.source_expressions[0])

        sql = """
            COALESCE(
                NULLIF(
                    CASE 
                        WHEN INSTR(%s, '/') > 0 AND INSTR(%s, '\\') > 0 THEN
                            CASE 
                                WHEN INSTR(%s, '/') > INSTR(%s, '\\') 
                                THEN SUBSTR(%s, 1, INSTR(%s, '/') - 1)
                                ELSE SUBSTR(%s, 1, INSTR(%s, '\\') - 1)
                            END
                        WHEN INSTR(%s, '/') > 0 THEN SUBSTR(%s, 1, INSTR(%s, '/') - 1)
                        WHEN INSTR(%s, '\\') > 0 THEN SUBSTR(%s, 1, INSTR(%s, '\\') - 1)
                        ELSE %s
                    END,
                    ''
                ),
                %s
            )
        """ % tuple([path] * 14)

        return sql, path_params * 14


class DirnameLookup(Lookup):
    """
    Lookup для фильтрации по директории пути
    Использование: MyModel.objects.filter(path__dirname='/home/user')
    """
    lookup_name = 'dirname'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        # Преобразуем путь в директорию с помощью Dirname
        dirname_expr = Dirname(models.F(lhs.target.name))
        dirname_sql, dirname_params = dirname_expr.as_sql(compiler, connection)

        # Строим условие сравнения
        params = dirname_params + rhs_params
        return f"{dirname_sql} = %s", params
