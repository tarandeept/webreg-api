from bs4 import BeautifulSoup
from collections import defaultdict
from datetime import datetime

'''
Example of tr containing course info
<tr valign="top" bgcolor="#FFFFCC">
    <td bgcolor="#D5E5FF"  nowrap="nowrap">34000</td>
    <td  nowrap="nowrap">Lec</td>
    <td bgcolor="#D5E5FF"  nowrap="nowrap">A</td>
    <td  nowrap="nowrap">4</td>
    <td bgcolor="#D5E5FF"  nowrap="nowrap">ZHAO, S.</td>
    <td  nowrap="nowrap">TuTh &nbsp; 11:00-12:20p</td>
    <td bgcolor="#D5E5FF"  nowrap="nowrap">VRTL REMOTE</td>
    <td  nowrap="nowrap">Tue, Dec 15, 10:30-12:30pm</td>
    <td bgcolor="#D5E5FF" align="right" nowrap="nowrap">150</td>
    <td align="right" nowrap="nowrap">128</td>
    <td bgcolor="#D5E5FF" align="right" nowrap="nowrap">n/a</td>
    <td align="right" nowrap="nowrap">259</td>
    <td bgcolor="#D5E5FF"  nowrap="nowrap">A</td>
    <td  nowrap="nowrap"><a href="http://uci.bncollege.com"  target="_blank">Bookstore</a></td>
    <td bgcolor="#D5E5FF"  nowrap="nowrap">&nbsp;</td>
    <td  nowrap="nowrap"><b><font color="green">OPEN</font></b></td>
</tr>
'''

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

def append_am_pm(time) -> str:
    '''Adds either AM or PM to input time string'''
    temp = time[-1].lower()
    if temp == 'a':
        time = time[0:-1] + 'AM'
    elif temp == 'am':
        time = time[0:-2] + 'AM'
    elif temp == 'p':
        time = time[0:-1] + 'PM'
    elif temp == 'pm':
        time = time[0:2] + 'PM'
    else:
        time = time + 'AM'
    return time

def extract_days(datetime) -> str:
    ### REVISIT THIS FUNCTION AND CHANGE IT TO RETURN A LIST OF DIGITS [0,1,2,3,4,5,6]
    '''Given a string in the format: TuTh   11:00-12:20p, returns TuTh'''
    return datetime.split()[0].strip()

def extract_start_end_time(str_time) -> {'start', 'end'}:
    '''Given a string in the format: TuTh   11:00-12:20p, returns a dict
    containing the start and end times as a Time object'''
    result = dict()
    str_time = str_time.split()[1].strip()
    result['start'] = append_am_pm(str_time.split('-')[0])
    result['end'] = append_am_pm(str_time.split('-')[1])
    return result

def add_course_to_course_dict(course_dict, course_info):
    '''Gives a dict containing course info, adds the course info to the course_dict'''
    keys = ['code', 'title', 'name', 'type', 'sec', 'units', 'instructor', 'days', 'start_time', 'end_time',
            'place', 'final', 'max', 'enr', 'wl', 'req', 'rstr', 'textbooks', 'web', 'status']

    code = course_info['code']
    for key in keys:
        course_dict[code][key] = course_info[key]

    print(course_dict[34000])

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
                # add_course_to_course_dict(course_dict, course_info)

if __name__ == '__main__':
    filename = 'html_files/compsci_2020_fall.html'
    course_dict = defaultdict(dict)
    construct_course_dict(course_dict, filename)
