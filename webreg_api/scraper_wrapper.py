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

Some Dept Parameters Values: (See depts below for full list of Dept Values)
- COMPSCI
- CHEM
- ARTS
"""
import requests
import os

BASE_URL = 'https://www.reg.uci.edu/perl/WebSoc/?YearTerm={YEAR-XX}&ShowComments=on&ShowFinals=on&Breadth=ANY&Dept={DEPT}&CourseNum=&Division=ANY&CourseCodes=&InstrName=&CourseTitle=&ClassType=ALL&Units=&Days=&StartTime=&EndTime=&MaxCap=&FullCourses=ANY&FontSize=100&CancelledCourses=Exclude&Bldg=&Room=&Submit=Display+Web+Results'
CURRENT_YEAR_TERM = '2021-92'
CURRENT_YEAR = '2021'
CURRENT_QTR = 'FALL'
DEPTS = ['AC ENG', 'AFAM', 'ANATOMY', 'ANESTH', 'ANTHRO', 'ARABIC', 'ARMN', 'ART', 'ART HIS', 'ARTS',
        'ARTSHUM', 'ASIANAM', 'BANA', 'BATS', 'BIO SCI', 'BIOCHEM', 'BME', 'BSEMD', 'CAMPREC', 'CBE',
        'CBEMS', 'CEM', 'CHC/LAT', 'CHEM', 'CHINESE', 'CLASSIC', 'CLT%26THY', 'COGS', 'COM LIT', 
        'COMPSCI', 'CRITISM', 'CRM/LAW', 'CSE', 'DANCE', 'DERM', 'DEV BIO', 'DRAMA', 'E ASIAN', 
        'EARTHSS', 'EAS', 'ECO EVO', 'ECON', 'ECPS', 'ED AFF', 'EDUC', 'EECS', 'EHS', 'ENGLISH', 
        'ENGR', 'ENGRCEE', 'ENGRMAE', 'ENGRMSE', 'EPIDEM', 'ER MED', 'EURO ST', 'FAM MED', 'FIN', 
        'FLM%26MDA', 'FRENCH', 'GDIM', 'GEN%26SEX', 'GERMAN', 'GLBL ME', 'GLBLCLT', 'GREEK', 'HEBREW', 
        'HINDI', 'HISTORY', 'HUMAN', 'HUMARTS', 'I%26C SCI', 'IN4MATX', 'INNO', 'INT MED', 'INTL ST', 
        'IRAN', 'ITALIAN', 'JAPANSE', 'KOREAN', 'LATIN', 'LAW', 'LINGUIS', 'LIT JRN', 'LPS', 'LSCI', 
        'M%26MG', 'MATH', 'MED', 'MED ED', 'MED HUM', 'MGMT', 'MGMT EP', 'MGMT FE', 'MGMT HC', 
        'MGMTMBA', 'MGMTPHD', 'MIC BIO', 'MOL BIO', 'MPAC', 'MSE', 'MUSIC', 'NET SYS', 'NEURBIO', 
        'NEUROL', 'NUR SCI', 'OB/GYN', 'OPHTHAL', 'PATH', 'PED GEN', 'PEDS', 'PERSIAN', 'PHARM', 
        'PHILOS', 'PHMD', 'PHRMSCI', 'PHY SCI', 'PHYSICS', 'PHYSIO', 'PLASTIC', 'PM%26R', 'POL SCI', 
        'PORTUG', 'PP%26D', 'PSCI', 'PSY BEH', 'PSYCH', 'PUB POL', 'PUBHLTH', 'RADIO', 'REL STD', 
        'ROTC', 'RUSSIAN', 'SOC SCI', 'SOCECOL', 'SOCIOL', 'SPANISH', 'SPPS', 'STATS', 'SURGERY', 
        'SWE', 'TAGALOG', 'TOX', 'UCDC', 'UNI AFF', 'UNI STU', 'UPPP', 'VIETMSE', 'VIS STD', 'WRITING']


DEPTS = ['COMPSCI', 'SOC SCI', 'CHEM']  # Only 3 depts used for testing. Comment this when running for all depts




def get_dept_courses(dept):
    url = BASE_URL.replace('{YEAR-XX}', CURRENT_YEAR_TERM)
    url = url.replace('{DEPT}', dept)
    response = requests.get(url)
    html = response.text
    return html

def get_course_files_and_save():
    base_path = os.getcwd() + f'/webreg_api/html_files/{CURRENT_YEAR}/{CURRENT_QTR}'
    for dept in DEPTS:
        file_path = base_path + f'/{dept}/{dept}.html'
        with open(file_path, 'w') as file:
            html = get_dept_courses(dept)
            file.write(html)

def create_dept_directories():
    base_path = os.getcwd() + f'/webreg_api/html_files/{CURRENT_YEAR}/{CURRENT_QTR}'
    for dept in DEPTS:
        dept_path = base_path + f'/{dept}'
        if not os.path.exists(dept_path):
            os.mkdir(dept_path)

def create_year_quarter_directory():
    year_path = os.getcwd() + f'/webreg_api/html_files/{CURRENT_YEAR}'
    quarter_path = year_path + f'/{CURRENT_QTR}'
    if not os.path.exists(year_path):
        os.mkdir(year_path)
    if not os.path.exists(quarter_path):
        os.mkdir(quarter_path)




if __name__ == '__main__':
    create_year_quarter_directory()
    create_dept_directories()
    get_course_files_and_save()
