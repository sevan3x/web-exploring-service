WEB EXPLORING SERVICE

The service's functuon is to explore websites, take screenshots and to store them.
The two main functualities are to explore a given website and the wanted number of links, and to search for already taken screenshot stored in the database.

Quick Guide:
1. To explore a website you just simply need to execute the following command:
   python screenshot_service.py -u [mainUrl] -n [numberOfPages]
2. To find an already take screenshot in the db execute:
   python screenshot_service.py -g [screenshotId]

The screenshots are stored in base64, instead of PNGs. This is with storage management purposes.

The DB is simple, having only 3 fields:
1. id - Primary Key, random-generated UUID
2. screenshot_data - the data of the screenshot converted with base64
3. taken_at - timestamp of when the screenshot was made
