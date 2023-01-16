# scripts

This directory contains all the script files used in setting up the app's environment.

## generate_authors.sh

Run this script to automatically create an AUTHORS file containing names and emails of all who have contributed to this project. The names and emails are extracted from the git logs.
__Note__: Run this script from the root directory (ie michote/) and not from the configs directory.
Example:

```bash
$ cd michote/
../michote/ $ ls
configs models .gitignore AUTHORS README.md
../michote/ $ ./configs/generate_authors.sh
../michote/ $
```

## setup_mysql_dev.sql

Run this script to create the database locally that will be used by the app. See example below to see how to run.
__Note__: Ensure mysql is installed first before running the script.

Example:

```bash
$ cd michote/
../michote/ $ cat setup_mysql_dev.sql | sudo mysql
Enter password:
../michote/ $
```
