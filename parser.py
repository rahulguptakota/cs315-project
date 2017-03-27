"""
FILE: skeleton_parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012
Skeleton parser for cs145 programming project 1. Has useful imports and
functions for parsing, including:
1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the xml files store dollar value amounts in 
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the xml files store dates/ times in the form 
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)
5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or 
is not of #PCDATA type)
6) A function to get all elements of a specific tag name that are children of a
given element
7) A function to get only the first such child
Your job is to implement the parseXml function, which is invoked on each file by
the main function. We create the dom for you; the rest is up to you! Get familiar 
with the functions at http://docs.python.org/library/xml.dom.minidom.html and 
http://docs.python.org/library/xml.dom.html
Happy parsing!
"""

import sys
import datetime
from xml.dom.minidom import parse
from re import sub
Itemsfile = open('Itmes', 'w')
Categoryfile = open('Category', 'w')
Userfile = open('Users','w')
Bidfile = open('Bid','w')
columnSeparator = "<>"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
                'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


"""
Returns true if a file ends in .xml
"""
def isXml(f):
    return len(f) > 4 and f[-4:] == '.xml'

"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
    elements = []
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            elements.append(child)
    return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            return child
    return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
        return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
    if len(elem.childNodes) == 1:
        return pcdata(elem) 
    return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
    curElem = getElementByTagNameNR(elem, tagName)
    if curElem != None:
        return pcdata(curElem)
    return ''

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon] 
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)

"""
Parses a single xml file. Currently, there's a loop that shows how to parse
item elements. Your job is to mirror this functionality to create all of the necessary SQL tables
"""
def parseXml(f):
    dom = parse(f) # creates a dom object for the supplied xml file
    Items = dom.getElementsByTagName('Item')
    users = []

    for item in Items:
        itemID = item.getAttribute('ItemID') #following code is for items 
        # if not itemID:
        #     itemID = 'NULL'
        Itemsfile.write(itemID+'`')
        totbids = getElementTextByTagNameNR(item,'Number_of_Bids')
        # if not totbids:
        #     totbids = 'NULL'
        Itemsfile.write(totbids+'`')
        firstBid = getElementTextByTagNameNR(item,'First_Bid')
        # if not firstBid:
        #     firstBid = 'NULL'
        Itemsfile.write(firstBid+'`')
        currently = getElementTextByTagNameNR(item,'Currently')
        # if not currently:
            # currently = 'NULL'
        Itemsfile.write(currently+'`')
        name = getElementTextByTagNameNR(item,'Name')
        if not name:
            name = 'NULL'
        name = name.replace('`', ' ')
        Itemsfile.write(name+'`')
        description = getElementTextByTagNameNR(item,'Description')
        description = str(description).replace('\"', ' ')
        description = str(description).replace('`', ' ')
        if not description:
            description = 'NULL'
        Itemsfile.write(description+'`')
        startTime = getElementTextByTagNameNR(item,'Started')
        if not startTime:
            startTime = 'NULL'
        else:
            #print startTime
            startTime = transformDttm(startTime)
            #print startTime
            startTime = str(startTime).replace('-',' ')
            startTime = str(startTime).replace(':',' ')
            startTime = str(startTime).split(' ')
       #     print startTime
            startTime = datetime.datetime(int(startTime[0]),int(startTime[1]),int(startTime[2]),int(startTime[3]),int(startTime[4]),int(startTime[5])).strftime('%s')
        #    print startTime
        Itemsfile.write(startTime+'`')
        endTime = getElementTextByTagNameNR(item,'Ends')
        if not endTime:
            endTime = 'NULL'
        else:
            #print startTime
            endTime = transformDttm(endTime)
            #print startTime
            endTime = str(endTime).replace('-',' ')
            endTime = str(endTime).replace(':',' ')
            endTime = str(endTime).split(' ')
        #    print endTime
            endTime = datetime.datetime(int(endTime[0]),int(endTime[1]),int(endTime[2]),int(endTime[3]),int(endTime[4]),int(endTime[5])).strftime('%s')
        #    print endTime

        Itemsfile.write(endTime+'`')
        userID = item.getElementsByTagName('Seller')[0].getAttribute('UserID')
        if not userID:
            userID = 'NULL'
        Itemsfile.write(userID+'\n')

        #following code is for categories
        categories = []
        for node in item.getElementsByTagName('Category'):
            category = getElementText(node)
            if (category not in categories):
                categories.append(category)
        for category in categories:
            Categoryfile.write(itemID + '`' + category + '\n')
        # following code is for Users
        seller = item.getElementsByTagName('Seller')[0]
        userID = seller.getAttribute('UserID')
        if userID not in users:
            users.append(userID)
            rating = seller.getAttribute('Rating')
            location = getElementTextByTagNameNR(item, 'Location')
            country = getElementTextByTagNameNR(item, 'Country')
            Userfile.write(userID + '`' + rating + '`' + location + '`' + country + '\n')
        #code for bidders
        for node1 in item.getElementsByTagName('Bids'):
            for node2 in node1.getElementsByTagName('Bid'):
                time = getElementTextByTagNameNR(node2 , 'Time')
                time = transformDttm(time)
                time = str(time).replace('-',' ')
                time = str(time).replace(':',' ')
                time = str(time).split(' ')
                time = datetime.datetime(int(time[0]),int(time[1]),int(time[2]),int(time[3]),int(time[4]),int(time[5])).strftime('%s')
                amount = getElementTextByTagNameNR(node2 , 'Amount')
                for node in node2.getElementsByTagName('Bidder'):
                    bidderid = node.getAttribute('UserID')
                    Bidfile.write(itemID + '`' + userID + '`' + time + '`' + amount + '\n')
       
        




    """
    TO DO: traverse the dom tree to extract information for your SQL tables
    """

"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_parser.py <path to xml files>'
        sys.exit(1)
    # loops over all .xml files in the argument
    for f in argv[1:]:
        if isXml(f):
            parseXml(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)