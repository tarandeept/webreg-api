from bs4 import BeautifulSoup
from collections import defaultdict
from utils import *
import pymysql

def is_course_title(tr) -> bool:
    '''Returns True if the tr contains the CourseTitle
    Example:
    <tr bgcolor="#fff0ff" valign="top">
        <td class="CourseTitle" colspan="16" nowrap="nowrap">&nbsp; CompSci &nbsp; 112 &nbsp; &nbsp; <font face="sans-serif"><b>COMPUTER GRAPHICS</b></font>&nbsp; &nbsp; &nbsp; (<a target='_blank' href='https://www.reg.uci.edu/cob/prrqcgi?term=202092&amp;dept=COMPSCI&amp;action=view_by_term#112'>Prerequisites</a>)</td>
    </tr>
    '''
    td = tr.find_next('td')
    return td.has_attr('class') and td['class'][0] == 'CourseTitle'

def extract_title_info(tr) -> {'title', 'name'}:
    '''Returns a dict that contains the title and name of the given tr
    Returns empty dict if the input was not valid
    '''
    result = dict()
    try:
        td = tr.find_next('td')
        title = td.text.split()
        course_title = title[0] + ' ' + title[1]
        course_name = td.b.text.strip()
        result['title'] = course_title
        result['name'] = course_name
        return result
    except:
        return dict()

def is_course_info(tr) -> bool:
    '''Returns True if the tr contains course info such as course code etc.'''
    tds = tr.find_all('td')
    return len(tds) == 16

def extract_info(td, key) -> str:
    '''Returns the info for the given td'''
    if key == 'textbooks' or key == 'web':
        url = td.find('a')
        if url and url.has_attr('href'):
            return url['href'].strip()
        else:
            return ''
    else:
        return td.text.strip()

def extract_course_info(tr) -> {'code', 'type', 'sec', 'units', ..., 'status'}:
    '''Returns a dict containing course info of the given tr
    Returns empty dict if input is invalid'''
    result = dict()
    keys = ['code', 'type', 'sec', 'units', 'instructor', 'time', 'place', 'final',
            'max', 'enr', 'wl', 'req', 'rstr', 'textbooks', 'web', 'status']
    try:
        tds = tr.find_all('td')
        for index, key in enumerate(keys):
            result[key] = extract_info(tds[index], key)
        result['code'] = int(result['code'])
        return result
    except:
        return dict()

def extract_start_end_time(str_time) -> {'start', 'end'}:
    '''Given a string in the format: TuTh   11:00-12:20p, returns a dict
    containing the start and end times as a Time object'''
    result = dict()
    time_range = extract_time_range(str_time)
    result['start'] = extract_start(time_range)
    result['end'] = extract_end(time_range)
    return result

def add_course_to_course_dict(course_dict, course_info):
    '''Gives a dict containing course info, adds the course info to the course_dict'''
    keys = ['code', 'title', 'name', 'type', 'sec', 'units', 'instructor', 'days', 'start_time', 'end_time',
            'place', 'final', 'max', 'enr', 'wl', 'req', 'rstr', 'textbooks', 'web', 'status']
    code = course_info['code']
    for key in keys:
        course_dict[code][key] = course_info[key]

def construct_course_dict(course_dict, filename):
    '''Inserts course info into course_dict'''
    with open(filename) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        courses = soup.find_all('tr', valign='top')
        course_title = None
        course_name = None
        for course in courses:
            if is_course_title(course):
                title_info = extract_title_info(course)
                course_title = title_info['title']
                course_name = title_info['name']
            elif is_course_info(course):
                course_info = extract_course_info(course)
                start_end_times = extract_start_end_time(course_info['time'])
                course_info['title'] = course_title
                course_info['name'] = course_name
                course_info['days'] = extract_days(course_info['time'])
                course_info['start_time'] = start_end_times['start']
                course_info['end_time'] = start_end_times['end']
                add_course_to_course_dict(course_dict, course_info)

if __name__ == '__main__':
    ### Setup MySQL connection to local db
    ### Need to eventually connect to DB hosted remotely
    ### Need to eventually create config file so as to not expose password
    ### Make sure to gitignore config file
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password='Shishkabobs',
                                db='uci_webreg',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
    cursor = connection.cursor()
    filename = 'html_files/compsci_2020_fall.html'
    course_dict = defaultdict(dict)
    construct_course_dict(course_dict, filename)
