.open auction.db
drop trigger if exists ENDTIME;
drop trigger if exists RECENTAMOUNT;
drop trigger if exists SELLERNOTBIDDER;
drop trigger if exists CORRECTBIDTIME;
drop trigger if exists BIDNUMBER;
drop trigger if exists BIDAMOUNT;

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