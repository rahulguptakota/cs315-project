.open auction.db
drop table if exists ITEMS;
drop table if exists CATEGORY;
drop table if exists USER;
drop table if exists BID;

CREATE TABLE ITEMS(
   itemID   INT PRIMARY KEY NOT NULL,
   totBids  INT NOT NULL,
   firstBid INT NOT NULL,
   currently    INT NOT NULL,
   name STRING,
   description  STRING,
   startTime    INT NOT NULL,
   endTime  INT NOT NULL,
   userID   STRING NOT NULL
);

CREATE TABLE CATEGORY(
   name STRING  NOT NULL,
   itemID   INT NOT NULL,
   PRIMARY KEY (name, itemID)
);

CREATE TABLE USER(
   userID   STRING  PRIMARY KEY NOT NULL,
   rating   INT,
   location STRING
);

CREATE TABLE BID(
   itemID   INT NOT NULL,
   userID   STRING NOT NULL,
   bidtime  INT NOT NULL,
   bidmoney INT NOT NULL,
   PRIMARY KEY (itemID, userID, bidtime)
);

