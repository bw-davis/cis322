cp -r src/* $HOME/wsgi
apachectl restart
cd sql
psql $1 -f create_tables.sql
