from orator import DatabaseManager

# Local Connection
config = {
    'mysql': {
        'driver'    : 'mysql',
        'host'      : 'localhost',
        'database'  : 'aplikasi_febyola_prediksi',
        'user'      : 'root',
        'password'  : '',
        'prefix'    : '',
        'charset'   : 'utf8mb4'
    }
}


db = DatabaseManager(config)
