import requests
import config

class google_sheets(object):
    classes = []
    sh = None
    A_chr = 65

    def __init__(self):
        pass

    def get_classes(self):    # return all classes
        self.res = requests.get('https://sheets.googleapis.com/v4/spreadsheets/{}?includeGridData=true&ranges={}&key={}'.format(config.GOOGLE_SHEET,"C4:S4",config.API_KEY))
        self.classes = []
        for i in self.res.json()["sheets"][0]["data"][0]["rowData"][0]["values"]:
            self.classes.append(i["formattedValue"])
        return self.classes


    def get_timetable(self, day, class_number): # day : 0 - Mon, 1 - Tue, 2 - Wed, 3 - Thu, 4 - Fri, 5 - Mon (next week)
        
        classes = self.get_classes()

        self.column = chr(67 + self.classes.index(class_number)) # self.column + str(self.row) + ":" + self.column + str(self.row + 8)
        self.row = 5 + (12 * day)
        print(self.column + str(self.row) + ":" + self.column + str(self.row + 8))
        res = requests.get('https://sheets.googleapis.com/v4/spreadsheets/{}?includeGridData=true&ranges={}&key={}'.format(config.GOOGLE_SHEET,self.column + str(self.row) + ":" + self.column + str(self.row + 8),config.API_KEY))


        res = res.json()["sheets"][0]["data"][0]["rowData"]

        timetable = []
        for i in res:
            lesson = [] # [№ of classroom, № of teacher, type] type: "Classroom hour", "Cancelled", "Changed"
            
            teacher_numer = i["values"][0]["formattedValue"]

            cell_color = []
            cell_color.append(i["values"][0]["userEnteredFormat"]["backgroundColor"]["red"])
            cell_color.append(i["values"][0]["userEnteredFormat"]["backgroundColor"]["green"])
            try:
                cell_color.append(i["values"][0]["userEnteredFormat"]["backgroundColor"]["blue"])
            except:
                cell_color.append(None)


            if teacher_numer == []:
                lesson.append(['-','-'])
            elif ('(1)' in teacher_numer) or ('(2)' in teacher_numer):
                lesson.append("-")
                lesson.append(teacher_numer)
            elif teacher_numer[-2:] != 'э)' and not("/" in teacher_numer) and not '(акт.з)' in teacher_numer:
                lesson.append(teacher_numer[-4:-1])
                lesson.append(teacher_numer[:-5])
            elif '(акт.з)' in teacher_numer:
                lesson.append(i[0][-6:-1])
                lesson.append(i[0][:-7])

            else:
                lesson.append("---")
                lesson.append(teacher_numer)
            
            
            if cell_color == [0.6431373, 0.7607843, 0.95686275]:
                lesson.append("Classroom hour")
            elif cell_color == [0.91764706, 0.6, 0.6]:
                lesson.append("Cancelled")
            elif cell_color == [1, 1, None]:
                lesson.append("Changed")
            else:
                lesson.append(None)

            timetable.append(lesson)
        return timetable


# google_sheets = google_sheets()
# print(google_sheets.get_timetable(0,"10"))

# [['5а', '5б', '5в', '6а', '6б', '6в', '6г', '7а', '7б', '7в', '8а', '8б', '8в', '9а', '9б', '10', '11']]