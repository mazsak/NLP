import re

with open('time.txt', 'r') as f:
    text = ' '.join(f.readlines())
r = re.compile(r'(\d{1,2}(:\d{2}){1,2})')

for index, match in enumerate(re.finditer(r, text)):
    print(str(index+1) + ". " + match.group())
