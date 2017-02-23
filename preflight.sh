cp src/* $HOME/wsgi
cd sql
psql $1 -f create_tables.sql