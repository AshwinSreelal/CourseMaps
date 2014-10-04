from course import Course
class Database:
    def __init__(self):
        self.courselist={}
    
    def add_course(self, name, course):
        self.courselist[name]=course
    
    def convert_file(self,name):
        course_file=open(name)
        for line in course_file:
            read = False
            i=0
            data=[]
            text=''
            for char in line:
                if char == "'":
                    if read:
                        read=False
                        data.append(text)
                        text=''
                        i+=1
                    else:
                        read=True
                elif read:
                    text+=char
            print(data)
            self.courselist[data[0]]= Course(data[0], data[1], int(data[2]), data[3].split(),data[4].split(),data[5].split())

    def get_course(self,name):
        return self.courselist[name]

    def get_prereq_courses(self,name):
        courses=[]
        for prereq in self.courselist[name].get_prereqs():
            courses.append(self.get_course(prereq))
        return courses 
