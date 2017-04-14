select userID from BID where userID not in (select userID from USER);
select userID from ITEMS where userID not in (select userID from USER);
select itemID from BID where itemID not in (select itemID from ITEMS);
select itemID from CATEGORY where itemID not in (select itemID from ITEMS);
select * from ITEMS where (starttime > endtime);