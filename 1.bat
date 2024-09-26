@echo off
echo Updating database...

rem Delete the existing database file
if exist site.db del site.db

rem Initialize the migration repository
flask db init

rem Create a migration
flask db migrate -m "Initial migration"

rem Apply the migration
flask db upgrade

rem Create an admin user
python create_admin.py

echo Database update complete.
pause