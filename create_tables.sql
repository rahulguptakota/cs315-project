.open auction.db
drop table if exists ITEMS;
drop table if exists CATEGORY;
drop table if exists USER;
drop table if exists BID;
drop table if exists TIME;
drop trigger if exists ENDTIME;
drop trigger if exists RECENTAMOUNT;
drop trigger if exists SELLERNOTBIDDER;
drop trigger if exists CORRECTBIDTIME;
drop trigger if exists BIDNUMBER;
drop trigger if exists BIDAMOUNT;

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
   endTime  INT NOT NULL,
   userID   STRING NOT NULL,
   FOREIGN KEY(userID) REFERENCES USER(userID)
);


create table TIME(
    currtime string PRIMARY KEY
    );

create trigger ENDTIME
after insert ON ITEMS
for each row
when exists(
	SELECT *
	FROM ITEMS
	WHERE itemID = new.itemID AND
	new.startTime >= new.endTime
)
begin
	select raise(rollback, 'An auction can not end before it starts!');
end;

create trigger RECENTAMOUNT
after insert ON BID
for each row
when exists(
	SELECT *
	FROM ITEMS
	WHERE itemID = new.itemID AND
	currently <> new.bidmoney
)
begin
	UPDATE ITEMS SET currently = new.bidmoney WHERE itemID = new.itemID;
end;

create trigger SELLERNOTBIDDER
after insert ON BID
for each row
when exists(
	SELECT *
	FROM ITEMS
	WHERE itemID = new.itemID AND
	userID = new.userID
)
begin
	select raise(rollback, 'Seller can not be bidder!');
end;

create trigger CORRECTBIDTIME
after insert ON BID
for each row
when exists(
	SELECT *
	FROM ITEMS
	WHERE itemID = new.itemID AND
    startTime > new.bidtime OR
	endTime < new.bidtime
)
begin
	select raise(rollback, 'This is not a time to bid buddy!');
end;

create trigger BIDNUMBER
after insert ON BID
for each row
when exists(
	SELECT *
	FROM ITEMS
	WHERE itemID = new.itemID AND
         totBids <> 
		(SELECT count(*)
		 FROM BID
		 WHERE itemID = new.itemID)
)
begin
	UPDATE ITEMS
	SET totBids = totBids + 1 
	WHERE itemID = new.itemID;
end;

create trigger BIDAMOUNT
after insert ON BID
for each row
when exists(
	SELECT *
	FROM BID
	WHERE itemID = new.itemID AND
	bidmoney >= new.bidmoney
)
begin
	select raise(rollback, 'BID amount is less than that of previous amount');
end;