"""
Custom Django database lookups.

Provides DirnameLookup for case-insensitive path prefix matching.

Пользовательские поисковые запросы Django.

Предоставляет DirnameLookup для нечувствительного к регистру поиска по префиксу пути.
"""

from django.db.models import Lookup


class DirnameLookup(Lookup):
    """
    Checks if field starts with a string (case-insensitive, with \\ to / replacement).

    Проверяет, начинается ли поле со строки (независимо от регистра, с заменой \\ на /).

    lookup_name = 'dirname'

    Example:
        MyModel.objects.filter(file_path__dirname='folder/subfolder')
    """
    lookup_name = 'dirname'

    def as_sql(self, compiler, connection):
        """
        Generate SQL for the lookup.

        Генерирует SQL для поискового запроса.

        Args:
            compiler: SQL compiler / Компилятор SQL
            connection: Database connection / Подключение к базе данных

        Returns:
            tuple: (sql_string, params) / (строка_sql, параметры)
        """
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        # PostgreSQL
        if connection.vendor == 'postgresql':
            sql = f"REPLACE(LOWER({lhs}), '\\', '/') LIKE LOWER(%s) || '%%'"
        # SQLite
        elif connection.vendor == 'sqlite':
            sql = f"REPLACE(LOWER({lhs}), '\\', '/') LIKE LOWER(%s) || '%'"
        # MySQL
        elif connection.vendor == 'mysql':
            sql = f"REPLACE(LOWER({lhs}), '\\\\', '/') LIKE CONCAT(LOWER(%s), '%%')"
        else:
            sql = f"REPLACE(LOWER({lhs}), '\\', '/') LIKE LOWER(%s) || '%%'"

        return sql, lhs_params + rhs_params
