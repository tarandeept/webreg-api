from bs4 import BeautifulSoup
from collections import defaultdict
from webreg_api import database, utils
import pymysql
import sys

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

def is_course_info(tr, header_len) -> bool:
    '''Returns True if the tr contains course info such as course code etc.'''
    tds = tr.find_all('td')
    return len(tds) == header_len

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

def extract_course_info(tr, keys) -> {'code', 'type', 'sec', 'units', ..., 'status'}:
    '''Returns a dict containing course info of the given tr
    Returns empty dict if input is invalid'''
    result = dict()
    try:
        tds = tr.find_all('td')
        for index, key in enumerate(keys):
            result[key] = extract_info(tds[index], key)
        result['code'] = int(result['code'])
        return result
    except:
        return dict()

def add_course_to_batch_params(batch_params, course_info):
    '''Gives a dict containing course info, adds the course info to the batch_params list'''
    keys = ['code', 'title', 'name', 'type', 'sec', 'units', 'instructor', 'days', 'start_time', 'end_time',
            'place', 'final', 'max', 'enr', 'wl', 'req', 'rstr', 'textbooks', 'web', 'status']
    entry = [None] * len(keys)
    for index, key in enumerate(keys):
        entry[index] = course_info[key]
    batch_params.append(entry)

def construct_batch_params(batch_params, headers, filename):
    '''Inserts course info into batch_params'''
    header_len = len(headers)
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
            elif is_course_info(course, header_len):
                course_info = extract_course_info(course, headers)
                course_info['title'] = course_title
                course_info['name'] = course_name
                course_info['days'] = utils.extract_days(course_info['time'])
                times = utils.extract_start_end_times(course_info['time'])
                course_info['start_time'] = times[0]
                course_info['end_time'] = times[1]
                add_course_to_batch_params(batch_params, course_info)

def batch_insert_courses(batch_params, cursor, table_name):
    '''Batch insers the courses into the DB'''
    query = f'INSERT INTO {table_name} \
            (code, title, name, type, sec, units, instructor, days, start_time, \
            end_time, place, final, max, enr, wl, req, rstr, textbooks, web, status) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.executemany(query, batch_params)

def find_course_count(filename):
    '''Finds how many courses are on the webpage'''
    with open(filename) as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        course_summary = soup.find('dl', class_='course-summary')
        count = course_summary.find('dt').text.split()[-1].strip()
        return int(count)

if __name__ == '__main__':
    ### Constants (headers may need to be adjusted per quarter)
    headers = ['code', 'type', 'sec', 'units', 'instructor', 'time', 'place', 'final',
                'max', 'enr', 'wl', 'req', 'nor', 'rstr', 'textbooks', 'web', 'status']

    ### Database setup
    config_file = '../config.ini'
    connection = database.setup_database_connection(config_file)
    cursor = connection.cursor()

    ### File setup
    year = sys.argv[1]
    quarter = sys.argv[2]
    filename = sys.argv[3]
    file = 'html_files/' + sys.argv[1]
    file = f'html_files/{year}/{quarter}/{filename}'

    ### Web scraping
    batch_params = []
    construct_batch_params(batch_params, headers, file)

    ### Metric tracking
    total_scraped_courses = len(batch_params)
    actual_course_count = find_course_count(file)
    print('---------------------------------------------------')
    print(f'Filename: ', file)
    print(f'Total Scraped Courses: {total_scraped_courses}')
    print(f'Actual course count: {actual_course_count}')
    print('Executing batch insertion')

    ### Inserting courses into database
    table_name = database.build_table_name(year, quarter)
    batch_insert_courses(batch_params, cursor, table_name)
    connection.commit()
    connection.close()
