sql: Bid Category Items Users
	sqlite3 < create_tables.sql
	sqlite3 < import_data.sql

gendata:
	python gen.py | bash

clean:
	[ -e Bid Category Items Users] && Bid Category Items Users