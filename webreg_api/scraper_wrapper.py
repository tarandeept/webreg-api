"""
This module is a wrapper for scraper.py
It is responsible for automatically running scraper.py 
for each department specified on the UCI webreg page.

UCI Webreg Base Form URL
https://www.reg.uci.edu/perl/WebSoc/?YearTerm=2021-92&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept=COMPSCI&CourseNum=&Division=ANY&CourseCodes=&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Web+Results
If you make a GET request to this URL, you will get the HTML content of all the classes
offered in Fall 2021 for the Department of COMPSCI

Of all these parameters, we really only care about YearTerm and Dept
In order to get HTML content for a different year/quarter and/or different Department, we will need to
change some of the URL parameters

Once we have the URL configured how we want it, we can GET the HTML content and run the scraper on it

YearTerm Parameters Values:
- YEAR-92 (Fall Quarter of the YEAR)
- YEAR-03 (Winter Quarter of the YEAR)
- YEAR-14 (Spring Quarter of the YEAR)

Some Dept Parameters Values: (See depts below for full list of Dept Values)
- COMPSCI
- CHEM
- ARTS
"""
import requests
import os
from scraper import run_scraper
import database

BASE_URL = 'https://www.reg.uci.edu/perl/WebSoc/?ShowComments=on&ShowFinals=on&Breadth=ANY&CourseNum=&Division=ANY&CourseCodes=&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Web+Results'
CURRENT_YEAR_TERM = '2021-92'
CURRENT_YEAR = '2021'
CURRENT_QTR = 'FALL'
DEPTS = ['AC ENG', 'AFAM', 'ANATOMY', 'ANESTH', 'ANTHRO', 'ARABIC', 'ARMN', 'ART', 'ART HIS', 'ARTS',
        'ARTSHUM', 'ASIANAM', 'BANA', 'BATS', 'BIO SCI', 'BIOCHEM', 'BME', 'BSEMD', 'CAMPREC', 'CBE',
        'CBEMS', 'CEM', 'CHC/LAT', 'CHEM', 'CHINESE', 'CLASSIC', 'CLT&THY', 'COGS', 'COM LIT', 
        'COMPSCI', 'CRITISM', 'CRM/LAW', 'CSE', 'DANCE', 'DERM', 'DEV BIO', 'DRAMA', 'E ASIAN', 
        'EARTHSS', 'EAS', 'ECO EVO', 'ECON', 'ECPS', 'ED AFF', 'EDUC', 'EECS', 'EHS', 'ENGLISH', 
        'ENGR', 'ENGRCEE', 'ENGRMAE', 'ENGRMSE', 'EPIDEM', 'ER MED', 'EURO ST', 'FAM MED', 'FIN', 
        'FLM&MDA', 'FRENCH', 'GDIM', 'GEN&SEX', 'GERMAN', 'GLBL ME', 'GLBLCLT', 'GREEK', 'HEBREW', 
        'HINDI', 'HISTORY', 'HUMAN', 'HUMARTS', 'I&C SCI', 'IN4MATX', 'INNO', 'INT MED', 'INTL ST', 
        'IRAN', 'ITALIAN', 'JAPANSE', 'KOREAN', 'LATIN', 'LAW', 'LINGUIS', 'LIT JRN', 'LPS', 'LSCI', 
        'M&MG', 'MATH', 'MED', 'MED ED', 'MED HUM', 'MGMT', 'MGMT EP', 'MGMT FE', 'MGMT HC', 
        'MGMTMBA', 'MGMTPHD', 'MIC BIO', 'MOL BIO', 'MPAC', 'MSE', 'MUSIC', 'NET SYS', 'NEURBIO', 
        'NEUROL', 'NUR SCI', 'OB/GYN', 'OPHTHAL', 'PATH', 'PED GEN', 'PEDS', 'PERSIAN', 'PHARM', 
        'PHILOS', 'PHMD', 'PHRMSCI', 'PHY SCI', 'PHYSICS', 'PHYSIO', 'PLASTIC', 'PM&R', 'POL SCI', 
        'PORTUG', 'PP&D', 'PSCI', 'PSY BEH', 'PSYCH', 'PUB POL', 'PUBHLTH', 'RADIO', 'REL STD', 
        'ROTC', 'RUSSIAN', 'SOC SCI', 'SOCECOL', 'SOCIOL', 'SPANISH', 'SPPS', 'STATS', 'SURGERY', 
        'SWE', 'TAGALOG', 'TOX', 'UCDC', 'UNI AFF', 'UNI STU', 'UPPP', 'VIETMSE', 'VIS STD', 'WRITING']


# DEPTS = ['COMPSCI', 'SOC SCI', 'CHEM']  # Only 3 depts used for testing. Comment this when running for all depts



def get_dept_courses(dept):
    '''Gets HTML course content for the given department'''
    payload = {'YearTerm': CURRENT_YEAR_TERM, 'Dept': dept}
    response = requests.get(BASE_URL, params=payload)
    html = response.text
    return html

def create_table(year, quarter):
    '''Creates the year quarter table if it doesn't exist'''
    connection = database.setup_database_connection()
    cursor = connection.cursor()
    sql = f'''CREATE TABLE IF NOT EXISTS `{year}_{quarter}_COURSES` (
    `code` int(11) NOT NULL,
    `title` varchar(100) DEFAULT NULL,
    `name` varchar(100) DEFAULT NULL,
    `type` varchar(10) DEFAULT NULL,
    `sec` varchar(10) DEFAULT NULL,
    `units` varchar(10) DEFAULT NULL,
    `instructor` varchar(100) DEFAULT NULL,
    `days` varchar(20) DEFAULT NULL,
    `start_time` varchar(10) DEFAULT NULL,
    `end_time` varchar(10) DEFAULT NULL,
    `place` varchar(100) DEFAULT NULL,
    `final` varchar(100) DEFAULT NULL,
    `max` int(11) DEFAULT NULL,
    `enr` varchar(20) DEFAULT NULL,
    `wl` varchar(10) DEFAULT NULL,
    `req` int(11) DEFAULT NULL,
    `rstr` varchar(20) DEFAULT NULL,
    `textbooks` varchar(100) DEFAULT NULL,
    `web` varchar(100) DEFAULT NULL,
    `status` varchar(20) DEFAULT NULL,
    `dept` varchar(50) DEFAULT NULL,
    PRIMARY KEY (`code`)
    )'''
    cursor.execute(sql)
    connection.commit()
    connection.close()

if __name__ == '__main__':
    create_table(CURRENT_YEAR, CURRENT_QTR)
    for dept in DEPTS:
        html = get_dept_courses(dept)
        run_scraper(CURRENT_YEAR, CURRENT_QTR, html, dept)
