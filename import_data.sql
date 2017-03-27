.separator `
.open auction.db
.import Itmes ITEMS
.import Category CATEGORY
.import Users USER
.import Bid BID

update ITEMS set name = null where name = "NULL";
update ITEMS set description = null where description = "NULL";
update ITEMS set name = null where name = "NULL";
update USER set rating = null where rating = "NULL";
update USER set location = null where location = "NULL";