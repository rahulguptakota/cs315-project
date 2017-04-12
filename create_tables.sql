.open auction.db
drop table if exists ITEMS;
drop table if exists CATEGORY;
drop table if exists USER;
drop table if exists BID;
drop table if exists TIME;

CREATE TABLE USER(
   userID   STRING  PRIMARY KEY NOT NULL,
   rating   INT,
   location STRING,
   country  STRING
);

CREATE TABLE CATEGORY(
   name STRING  NOT NULL,
   itemID   INT NOT NULL,
   PRIMARY KEY (name, itemID),
   FOREIGN KEY(itemID) REFERENCES ITEMS(itemID)
);

CREATE TABLE BID(
   itemID   INT NOT NULL,
   userID   STRING NOT NULL,
   bidtime  INT NOT NULL,
   bidmoney REAL NOT NULL,
   UNIQUE(itemID,bidtime),
   UNIQUE(itemID, userID,bidmoney),
   PRIMARY KEY (itemID, userID, bidtime),
   FOREIGN KEY(userID) REFERENCES USER(userID),
   FOREIGN KEY(itemID) REFERENCES ITEMS(itemID)
);

CREATE TABLE ITEMS(
   itemID   INT PRIMARY KEY NOT NULL,
   totBids  INT NOT NULL,
   firstBid INT NOT NULL,
   currently    INT NOT NULL,
   name STRING,
   description  STRING,
   startTime    INT NOT NULL,
   endTime  INT NOT NULL check(endTime > startTime),
   userID   STRING NOT NULL,
   FOREIGN KEY(userID) REFERENCES USER(userID)
);

create table TIME(
    currtime INT PRIMARY KEY
    );

