from django.db.models import Lookup


class DirnameLookup(Lookup):
    """Проверяет, начинается ли поле со строки (независимо от регистра, с заменой \\ на /)"""
    lookup_name = 'dirname'

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)

        # Функция для замены обратных слешей на прямые и приведения к нижнему регистру
        # Для PostgreSQL
        if connection.vendor == 'postgresql':
            sql = f"REPLACE(LOWER({lhs}), '\\', '/') LIKE LOWER(%s) || '%%'"
        # Для SQLite
        elif connection.vendor == 'sqlite':
            sql = f"REPLACE(LOWER({lhs}), '\\', '/') LIKE LOWER(%s) || '%'"
        # Для MySQL
        elif connection.vendor == 'mysql':
            sql = f"REPLACE(LOWER({lhs}), '\\\\', '/') LIKE CONCAT(LOWER(%s), '%%')"
        else:
            sql = f"REPLACE(LOWER({lhs}), '\\', '/') LIKE LOWER(%s) || '%%'"

        return sql, lhs_params + rhs_params
