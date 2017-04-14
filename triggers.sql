.open auction.db
drop trigger if exists RECENTAMOUNT;
drop trigger if exists SELLERNOTBIDDER;
drop trigger if exists CORRECTBIDTIME;
drop trigger if exists BIDNUMBER;
drop trigger if exists BIDAMOUNT;

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

create trigger CORRECTBIDTIME
after insert ON BID
for each row
when exists(
	SELECT *
	FROM ITEMS
	WHERE itemID = new.itemID AND
    (startTime > new.bidtime OR
	endTime < new.bidtime)
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
before insert ON BID
for each row
when exists(
	SELECT * from BID where (itemID = new.itemID AND bidmoney >= new.bidmoney)
)
begin
	select raise(rollback, 'BID amount is less than that of previous amount');
end;