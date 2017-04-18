all: gendata sql clean

gendata:
	python gen.py | bash

clean:
	rm Bid Category Items Users

sql: Users Items Bid Category
	sqlite3 < create_tables.sql
	sqlite3 < import_data.sql
	sqlite3 < triggers.sql
