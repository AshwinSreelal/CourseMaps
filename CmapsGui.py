import tkinter, database, course, random
class CmapsGui(tkinter.Tk):

    """
    Initialize window to unresizable width and height, and creates a database that reads
    and stores the courses.
    """
    def __init__(self, parent):

        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.w, self.h, self.sSize = 1280, 720, 40
        self.geometry("{}x{}".format(str(self.w), str(self.h)))
        self.resizable(False, False)
        self.database = database.Database()
        self.currentCourse = None
        self.database.convert_file("data.txt")
        self.init()

    """
    Sets a grid of widgets with course entry field on the top left, quit button on the
    top right, tree display canvas on the left, and course information (along with
    related courses) on the right.
    """
    def init(self):
        
        #Organize window into grid pattern
        self.grid()
        
        #Create course entry field widget in top left
        self.entryValue = tkinter.StringVar()
        self.courseEntry = tkinter.Entry(self, textvariable = self.entryValue)
        self.courseEntry.grid(column = 0, row = 0, sticky = "EW")
        self.courseEntry.bind("<Return>", self.OnCourseEntry)

        #Create quit button in top right
        self.quitButton = tkinter.Button(self, text = "Quit", command = self.quit)
        self.quitButton.grid(column = 1, row = 0, sticky = "NE", padx = 20)

        #Create display to show tree mapping of courses
        self.disp_w = 2 * self.w // 3
        self.display = tkinter.Canvas(self, width = self.disp_w, height = self.h)
        self.display.grid(column = 0, row = 1)

        #Create area to show course descriptioni
        self.info_w = self.w // 3
        self.courseInfo = tkinter.Canvas(self, width = self.info_w, height = self.h)
        self.courseInfo.grid(column = 1, row = 1, sticky = "NW")

        #Declare instance variables and initialize them to placeholder values
        self.courseRect = self.display.create_rectangle(0, 0, 0, 0, fill = "white")
        self.courseText = self.display.create_text(0, 0, text = "")
        self.coursePrereqRects = []
        self.courseFollowRects = []
        self.infoText = self.courseInfo.create_text(0, 0, text = "")
        self.relatedCourses =[]
        self.colorDict={}


    """
    Called when user enters a string into the text field and if the value evaluates
    to a valid course, calls the function to print the course tree.
    """
    def OnCourseEntry(self, event):

        try:
            self.currentCourse = self.database.get_course(self.entryValue.get().upper())
        except KeyError:
            print("Invalid Course Title")
    
        self.printCourseTree(self.currentCourse)
        
    """
    Prints out the entire course tree by printing out the course button, an iterated list of
    followup course buttons, and a recursively called iterated list of the entire trace of
    prerequisites. The buttons are visually organised in their relative position in the tree
    hierarchy. Additionally, prints out the course information on the right side and, if
    applicable, any related courses.
    """
    def printCourseTree(self, course):

        #Sets current course to the course to be displayed
        self.currentCourse = course

        #Checks if the current score is not a null value
        if self.currentCourse:
            #Clear display of previous course tree display
            self.display.delete(self.courseRect)
            self.display.delete(self.courseText)
            self.courseInfo.delete(self.infoText)
            for follow in self.courseFollowRects:
                for icon in follow:
                    self.display.delete(icon)
            for prereq in self.coursePrereqRects:
                for icon in prereq:
                    self.display.delete(icon)
            for related in self.relatedCourses:
                    self.courseInfo.delete(related)

            #Prints out course info on the right side of the window
            self.infoText = self.courseInfo.create_text(self.info_w // 8, self.h // 16, anchor = "nw", 
                                                        text = self.currentCourse.get_title() + "\n" + "Units: " + str(self.currentCourse.get_num_units()) + "\n\n" + self.currentCourse.get_courseinfo(), 
                                                        width = (3 * self.info_w) // 4)
            
            #Prints out a list of buttons pointing to all related courses, if applicable
            relateds = self.database.get_related_courses(self.currentCourse.get_title())
            relatedsLength = len(relateds)
            self.relatedCourses.append(self.courseInfo.create_text(self.info_w // 4, (9 * self.h) // 20, text = "Related Courses: "))
            for i in range(relatedsLength):
                self.relatedCourses.append(self.courseInfo.create_window(self.info_w // 4 + (self.info_w * 3 * i) // 16, self.h // 2, 
                                           window = tkinter.Button(self, text = relateds[i].get_title(), fg = "green", command = self.OnButtonClick(relateds[i]))))

            #Prints out a list of followup courses and lines to connect them to the current course
            scale = 70
            followups = self.database.get_followup_courses(self.currentCourse.get_title())
            followLength = len(followups)
            for i in range(followLength):
                width_center = (self.disp_w * (2 * i + 1)) // (2 * followLength)
                temp = []
                temp.append(self.display.create_window(width_center, (self.h // 8) - scale,
                                                       window = tkinter.Button(self, text = followups[i].get_title(),fg = "blue", command = self.OnButtonClick(followups[i]))))
                temp.append(self.display.create_line(width_center, (self.h // 8) - scale + self.sSize // 2,
                                                     self.disp_w // 2, self.h // 8 - self.sSize // 2))
                self.courseFollowRects.append(temp)

            """
            A recursive method that prints out all the prerequisite courses and their connection to the current course,
            and then recursively calls itself on the prerequisites of the prerequisite courses.
            """
            def printPreReqs(preReqs, level, widthleft, widthright):

                preReqLength = len(preReqs)
                for i in range(preReqLength):
                    width_center = widthleft + (widthright - widthleft) * (2 * i + 1) // (2 * preReqLength)
                    temp = []
                    temp.append(self.display.create_window(width_center, (self.h // 8) + scale * level,
                                                          window = tkinter.Button(self, text = preReqs[i].get_title(),
                                                          fg = self.colorForeground(level), bg = self.colorBackground(preReqs[i].get_title()),
                                                          command = self.OnButtonClick(preReqs[i]))))
                    if(level):
                        temp.append(self.display.create_line(width_center, (self.h // 8) + scale * level - self.sSize // 2, 
                                                             widthleft + (widthright - widthleft) // 2, self.h // 8 + scale * (level - 1) + self.sSize // 2))
                    self.coursePrereqRects.append(temp)
                    preReq2 = self.database.get_prereq_courses(preReqs[i].get_title())
                    if len(preReq2):
                        printPreReqs(preReq2, level + 1, widthleft + ((widthright - widthleft) * i) // len(preReqs), 
                                     widthleft + ((widthright - widthleft) * (i + 1)) // len(preReqs))
            
            #Initiates the resursive call by passing in the current course as the first argument
            printPreReqs([self.currentCourse], 0, 0,self.disp_w)

    """
    Gives an item a random colored background to improve the aesthetics of the
    display of the program
    """
    def colorBackground(self, classname):

        if classname in self.colorDict:
            return self.colorDict[classname]
        else:
            r = lambda: random.randint(128,255)
            self.colorDict[classname]=('#%02X%02X%02X' % (r(),r(),r()))
        return self.colorDict[classname]
    
    """
    Colors the foreground dark blue if the button is the current course, and colors it
    black otherwise.
    """
    def colorForeground(self,level):
        if level:
            return "black"
        else:
            return "dark blue"

    """
    Called when a button is clicked and returns a function that prints a new course tree display
    around the course associated with the button pressed.
    """
    def OnButtonClick(self, course):
        return lambda: self.printCourseTree(course)

#Runs the main process of the progam
if __name__ == "__main__":
    app = CmapsGui(None)
    app.title("Course Map")
    app.mainloop()
