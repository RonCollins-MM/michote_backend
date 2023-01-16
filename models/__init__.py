#!/usr/bin/python3

"""
This initialization module is responsible for creating a variable that holds
an instance of the storage engine class.

The storage type is set as an environment variable called `MICHOTE_TYPE_STORAGE`
Two storage types exist:
    1. File storage - Which is the default type storage when no type storage is
        specified.
    2. Database storage - The database in use is MySQL database.
"""

from os import getenv

storage_type = getenv('MICHOTE_TYPE_STORAGE')


if storage_type == 'db':
    from models.engine.db_storage import DB_Storage
    storage = DB_Storage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
