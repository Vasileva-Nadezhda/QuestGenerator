import database

if __name__ == '__main__':
    database.startup_db_client()
    database.shutdown_db_client()