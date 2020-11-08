from datetime import datetime

def row_print(row):
    '''Nicely prints a row in a dict'''
    for k,v in row.items():
        print(f'{k} | {v}')

def extract_days(datetime) -> str:
    ### REVISIT THIS FUNCTION AND CHANGE IT TO RETURN A LIST OF DIGITS [0,1,2,3,4,5,6]
    '''Given a string in the format: TuTh   11:00-12:20p, returns TuTh'''
    return datetime.split()[0].strip()

def extract_time_range(str_time):
    '''Given a string in the format: TuTh   11:00-12:20p, returns 11:00-12:20p
    If input is invalid returns the input'''
    try:
        return str_time.split()[1].strip()
    except:
        return str_time

def append_am_pm(time) -> str:
    '''Adds either AM or PM to input time string'''
    try:
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
    except:
        return None

def extract_start(str_time):
    '''Returns a Time object representing the start time. If time is TBA, returns None'''
    try:
        str_start = append_am_pm(str_time.split('-')[0])
        result = datetime.strptime(str_start, '%H:%M%p').time()
        return result
    except:
        return None

def extract_end(str_time):
    '''Returns a Time object representing the end time. If time is TBA, returns None'''
    try:
        str_end = append_am_pm(str_time.split('-')[1])
        return datetime.strptime(str_end, '%H:%M%p').time()
    except:
        return None
