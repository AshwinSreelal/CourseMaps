
class Course:
    """A course is an object defined by its title, course info, number of units, the classes it has a prereqs for
    the ones that it is a prereq of and courses it is related to
    self must be a string with no spaces, course_info must be a string with no apostrophes,num_units must be an int or float
    prereqs,followups, related_courses, must all be lists of strings although they can be empty lists"""
    def __init__(self,title, course_info, num_units, prereqs, followups, related_courses):
        self.title = title
        self.course_info = course_info
        self.num_units = num_units
        self.prereqs = prereqs
        self.followups = followups
        self.related_courses = related_courses
    
    """Returns the course title """
    def get_title(self):
        return self.title

    """Returns the string that is the course info """
    def get_courseinfo(self):
        return self.course_info

    """ Returns an int or float, the number of units of the course"""
    def get_num_units(self):
        return self.num_units

    """Returns a list of the prereqs of the course"""
    def get_prereqs(self):
        return self.prereqs

    """ Returns a list of the following courses of the course """
    def get_followups(self):
        return self.followups

    """Returns a list of the related courses of the course"""
    def get_related_courses(self):
        return self.related_courses

    """Allows for the addition of a new prereq for the course """
    def add_prereq(self,new_prereq):
        self.prereqs.append(new_prereq)

    """Allows for the addition of a new follow ups for the course """ 
    def add_followup(self,new_followup):
        self.followups.append(new_followup)
    
    """ Allows for the addition of a new related course"""
    def add_related_course(self,new_related):
        self.related_courses.append(new_related)
