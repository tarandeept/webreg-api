# import re

# result = []
# pattern = r'value=\"(.*)\"'
# file = open('hello.txt', 'r')

# for line in file.readlines():
#     match = re.search(pattern, line)
#     dept = match.group(1)
#     dept = dept.replace('&amp;', '%26')
#     result.append(dept)

# print(result)