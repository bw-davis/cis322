cp -r src/* $HOME/wsgi
psql $1 -f sql/create_tables.sql
