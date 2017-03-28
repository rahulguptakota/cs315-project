all: gendata sql clean

gendata:
	python gen.py | bash

clean:
	rm auction.db
	rm Users
	rm Category
	rm Bid
	rm Items
	[ -e Bid Category Items Users] && Bid Category Items Users

sql: Users Items Bid Category
	sqlite3 < create_tables.sql
	sqlite3 < import_data.sql
	sqlite3 < triggers.sql
