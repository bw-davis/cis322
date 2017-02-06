cd sql
psql $1 -f create_tables.sql
pip3 install Flask
cd ../src
python3 app.py