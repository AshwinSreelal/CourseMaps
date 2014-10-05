from course import Course
class Database:
    """ Initializes an empty dictionary for use as a database"""
    def __init__(self):
        self.courselist = {}
    
    """
    Converts a formatted file into a set of Course objects.
    The file must be formatted in the following manner:

    'course1_title' 'Description of course1' '#units' 'prereq1 prereq2' 'following1 following 2' 'related1 related2'
    'course2_title' 'Description of course2' '#units' 'prereq1 prereq2' 'following1 following 2' 'related1 related2'
    ...
    Note that the last 3 fields are allowed to be empty, and that no " ' " (apostrophe) should be used in the description  
    """ 

    def convert_file(self,name):
        #Uses python's native file reader to open a formatted data file
        course_file = open(name)

        #Reads the output line by line
        for line in course_file:
            read = False
            i = 0
            data = []
            text = ''
            #The following block goes through each character in the line, alternating reading and not reading when it hits a " ' "
            for char in line:
                if char == "'":
                    if read:
                        read = False
                        data.append(text)
                        text = ''
                        i += 1
                    else:
                        read = True
                elif read:
                    text += char

            #After this process, a list of strings is formed, with the lists of prereqs and the like seperated by spaces
            #For each line the courselist adds a course, with the title of the course as the key for the dictionary
            self.courselist[data[0]] = Course(data[0], data[1], int(data[2]), data[3].split(),data[4].split(),data[5].split())

    """This method enables the addition of courses into the database dictionary"""
    def add_course(self, name, course):
        self.courselist[name] = course
    
    """This method will retrieve a Course object given its name"""
    def get_course(self,name):
        return self.courselist[name]
    
    """ This method will output a list of the Course objects that are the input course's prerequisites"""
    def get_prereq_courses(self,name):
        courses = []
        for prereq in self.courselist[name].get_prereqs():
            if prereq in self.courselist:
                courses.append(self.get_course(prereq))
        return courses

    """ This method will output a list of the Course objects that are the input course's classes it is a prerequisite for"""
    def get_followup_courses(self, name):
        courses = []
        for follow in self.courselist[name].get_followups():
            if follow in self.courselist:
                courses.append(self.get_course(follow))
        return courses

    """ This method will output a list of the Course objects that are the input course's related courses"""
    def get_related_courses(self,name):
        courses=[]
        for related in self.courselist[name].get_related_courses():
            if related in self.courselist:
                courses.append(self.get_course(related))
        return courses
