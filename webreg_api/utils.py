from datetime import datetime, timedelta

def row_print(row):
    '''Nicely prints a row in a dict'''
    for k,v in row.items():
        print(f'{k} | {v}')

def extract_days(datetime) -> str:
    ### REVISIT THIS FUNCTION AND CHANGE IT TO RETURN A LIST OF DIGITS [0,1,2,3,4,5,6]
    '''Given a string in the format: TuTh   11:00-12:20p, returns TuTh'''
    return datetime.split()[0].strip()

def append_am_pm(time) -> str:
    '''Adds either AM or PM to input time string. AM by default'''
    try:
        temp = time[-1].lower()
        if temp == 'p':
            time = time[0:-1] + 'PM'
        elif temp == 'pm':
            time = time[0:2] + 'PM'
        else:
            time = time + 'AM'
        return time
    except:
        return None

def extract_start_end_times(str_time) -> []:
    '''Returns a list of Time objects. Index 0 is the start time. Index 1 is the end time'''
    start = extract_start_time(str_time)
    end = extract_end_time(str_time)
    try:
        diff = end - start
        minutes = diff.total_seconds() / 60
        if minutes > 300:
            start = start + timedelta(hours = 12)
        return [start.time(), end.time()]
    except:
        return [start, end]

def extract_start_time(str_time):
    '''Returns a Time object representing the start time. If time is TBA, returns TBA'''
    try:
        time_range = str_time.split('-')
        time = time_range[0].split()[1].strip()
        start = append_am_pm(time)
        result = datetime.strptime(start, '%I:%M%p')
        return result
    except:
        return str_time

def extract_end_time(str_time):
    '''Returns a Time object representing the end time. If time is TBA, returns TBA'''
    try:
        time_range = str_time.split('-')
        time = time_range[1].strip()
        end = append_am_pm(time)
        result = datetime.strptime(end, '%I:%M%p')
        return result
    except:
        return str_time
