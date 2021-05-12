"""
This module is a wrapper for scraper.py
It is responsible for automatically running scraper.py 
for each major specified on the UCI course page.

UCI Webreg Base Form URL
https://www.reg.uci.edu/perl/WebSoc/?YearTerm=2021-92&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=COMPSCI&CourseNum=&Division=ANY&CourseCodes=&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Web+Results
If you make a GET request to this URL, you will get the HTML content of all the classes
offered in Fall 2021 for the Department of COMPSCI

Of all these parameters, we really only care about YearTerm and Dept
In order to get HTML content for a different year/quarter and/or different Department, we will need to
change some of the URL parameters

Once we have the URL configured how we want it, we can GET the HTML file, save it, and run the scraper on it

YearTerm Parameters Values:
- YEAR-92 (Fall Quarter of the YEAR)
- YEAR-03 (Winter Quarter of the YEAR)
- YEAR-14 (Spring Quarter of the YEAR)

Some Dept Parameters Values: (See HTML for full list of Dept Values)
- COMPSCI
- CHEM
- ARTS
"""