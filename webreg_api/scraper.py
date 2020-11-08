from bs4 import BeautifulSoup
from collections import defaultdict

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

if __name__ == '__main__':
    course_dict = dict()

    with open('html_files/compsci_2020_fall.html') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        courses = soup.find_all('tr', valign='top')
        for course in courses:
            course_title = None
            course_name = None
            if is_course_title(course):
                title_info = extract_title_info(course)
                course_title = title_info['title']
                course_name = title_info['name']
            elif is_course_info(course):
                course_info = extract_course_info(course)
                for k,v in course_info.items():
                    print(f'Key: {k}   ---->{v}')
                # exit()
