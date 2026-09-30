"""
config/__init__.py

Configura pymysql como adaptador de MySQL si mysqlclient no está
disponible. Esto es un fallback útil para entornos donde mysqlclient
es difícil de compilar (ej: Windows sin build tools).
En EC2 (Ubuntu) se usa mysqlclient directamente.
"""
try:
    import mysqlclient
except ImportError:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
