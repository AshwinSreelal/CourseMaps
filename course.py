
class Course:
    def __init__(self,title, course_info, num_units,prereqs, postreqs, related_courses):
        self.title = title
        self.course_info = course_info
        self.num_units = num_units
        self.prereqs = prereqs
        self.postreqs = postreqs
        self.related_courses = related_courses
    
    def get_title(self):
        return self.title

    def get_courseinfo(self):
        return self.course_info

    def get_num_units(self):
        return self.num_units

    def get_prereqs(self):
        return self.prereqs

    def get_postreqs(self):
        return self.postreqs

    def get_related_courses(self):
        return self.related_courses

    def add_prereq(self,new_prereq):
        self.prereqs.append(new_prereq)

    def add_postreq(self,new_postreq):
        self.postreqs.append(new_postreq)

    def add_related_course(self,new_related):
        self.related_courses.append(new_related)
