make gendata 
make sql
cd cgi-bin
python auctionbase.py 8080
run localhost:8080 on your local browser and enjoy the auction




# cs315-project

Structure -> <br><br>
      Items (itemID, totBids, firstBid, currently, name, description, startTime, endTime, userID). <br>
      keys (itemID)<br><br>
      Category (name, itemID).<br>
      keys (name, itemID)<br><br>
      User (userID, rating, location).<br>
      keys (userID)<br><br>
      Bid (itemID, userID, time, money).<br>
      keys (itemID, userID, time)<br><br>
