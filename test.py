message_shedule = ''
shedule = [['208', '39', 'Classroom hour'], ['-', '39/ 22(эл б)', None], ['307', '22', None], ['303', '9', None], ['с.з', '28', None], ['-', '20(310)/11/38', None]]
for i in shedule:
    row = ''
    space = 1 + i[1].count(')') + i[1].count('(') + i[1].count('/')
    if i[2] == 'Classroom hour':
        row = '__{} ➖ {}__ \n'.format(i[1].ljust(22,' '),i[0])# parse_mode="Markdown"
    if i[2] == 'Changed':
        row = '**{} ➖ {}** \n'.format(i[1].ljust(22,' '),i[0])
    if i[2] == 'Cancelled':
        row = '~~{} ➖ {}~~ \n'.format(i[1].ljust(22,' '),i[0])
    else:
        row = '  {} ➖ {}   \n'.format(i[1].ljust(22,' '),i[0])
    message_shedule += row
print(message_shedule)