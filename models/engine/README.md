# Storage Engine

This directory contains the modules that handle storage engine of Michote.

Two storage engines exist:

    1. Database storage - handled by the `db_storage.py` module
    2. File storage - handled by the `file_storage.py` module

The two storage types are switched using an environment variable `MICHOTE_TYPE_STORAGE` when launching the server from terminal.
