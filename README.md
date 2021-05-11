Webreg API is an API that provides course info for courses available at UCI.
Currently this API can only return info for courses that will be available for
the upcoming 2021 Winter Quarter.

Endpoints:
Get course info
POST https://webreg-api.herokuapp.com/
Body:
- "code" (Integer representing the course code)
- "year" (Integer representing the year of the course)
- "quarter" (String {"fall", "winter", or "spring"})

How this API works:
This application has 3 main components
1. Course webscraper to gather course info
2. MySQL database to store course info
3. Flask API to serve course info

Web Scraper:
To run the webscraper
python scraper.py [year] [quarter] [filename]
python scraper.py 2021 winter compsci.html

Important Notes:
- Each quarter the UCI webreg uses 1 or 2 different headers to describe courses
For example 2021 Winter Quarter the headers used are (17 total)
(Code, Type, Sec, Units, Instructor, Time, Place, Final, Max, Enr, Wl, Req, Nor, Rstr, Textbooks,
Web, Status)
Fall 2020 however only used 16 headers (all the same besides for Nor)
- So because of this, each quarter the scraper.py needs to be adjusted to use the correct headers
