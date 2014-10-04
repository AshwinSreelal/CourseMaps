import tkinter, database, course, random
class CmapsGui(tkinter.Tk):
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

    def init(self):
        self.grid()
        
        self.entryValue = tkinter.StringVar()
        self.courseEntry = tkinter.Entry(self, textvariable = self.entryValue)
        self.courseEntry.grid(column = 0, row = 0, columnspan = 3, sticky = "EW")
        self.courseEntry.bind("<Return>", self.OnCourseEntry)

        self.display = tkinter.Canvas(self, width = self.w // 2, height = self.h)
        self.display.config(scrollregion = [0, 0, self.w // 2, self.h * 2])
        self.dispScrollBar = tkinter.Scrollbar(self, orient = "vertical", command = self.display.yview)
        self.display.configure(yscrollcommand = self.dispScrollBar.set)
        self.display.grid(column = 1, row = 1)
        self.dispScrollBar.grid(column = 0, row = 1, sticky = "NS")
        self.display.create_line(self.w // 2, 0, self.w // 2, self.h)

        self.courseRect = self.display.create_rectangle(0, 0, 0, 0, fill = "white")
        self.courseText = self.display.create_text(0, 0, text = "")
        self.coursePrereqRects = []
        self.courseFollowRects = []
        self.courseInfo = tkinter.Canvas(self, width = self.w // 2, height = self.h//4)
        self.courseInfo.grid(column = 2, row = 1)
        self.infoText = self.courseInfo.create_text(0, 0, text = "")
        self.relatedCourses =[]
        self.quitButton = tkinter.Button(self, text='Quit',command=self.quit)
        self.quitButton.grid(column= 2, row=1, sticky = "NE", padx=20)
        self.colorDict={}
    def OnCourseEntry(self, event):
        try:
            self.currentCourse = self.database.get_course(self.entryValue.get().upper())
        except KeyError:
            print("Invalid Course Title")
        self.printCourseTree(self.currentCourse)
               
    def printCourseTree(self, course):
        self.currentCourse = course
        if self.currentCourse:
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
            self.infoText = self.courseInfo.create_text(100, 100, anchor = "nw", 
                                                        text = "Units: " + str(self.currentCourse.get_num_units()) + "\n\n" + self.currentCourse.get_courseinfo(), 
                                                        width = self.w // 2 - 200)
            relateds=self.database.get_related_courses(self.currentCourse.get_title())
            relatedsLength = len(relateds)
            self.relatedCourses.append(self.courseInfo.create_text(self.w//4,25, text="RELATED COURSES: "))
            for i in range(relatedsLength):
                self.relatedCourses.append(self.courseInfo.create_window(25+(self.w-25)*(i+1)//(4*relatedsLength) ,50,window=tkinter.Button(self,text=relateds[i].get_title(),
                                     fg="green", command = self.OnButtonClick(relateds[i]))))
            scale = 80
            followups = self.database.get_followup_courses(self.currentCourse.get_title())
            followLength = len(followups)
            for i in range(followLength):
                width_center = (self.w * (2 * i + 1)) // (4 * followLength)
                temp = []
                temp.append(self.display.create_window(width_center, (self.h // 2) - scale,
                                                       window = tkinter.Button(self, text = followups[i].get_title(),fg="blue", command = self.OnButtonClick(followups[i]))))
                temp.append(self.display.create_line(width_center, (self.h // 2) - scale + self.sSize // 2,
                                                     self.w // 4, self.h // 2 - self.sSize // 2))
                self.courseFollowRects.append(temp)

            #self.display.create_window(self.w // 4, self.h // 2, window = tkinter.Button(self, text = self.currentCourse.get_title(), command = self.OnButtonClick(self.currentCourse)))

            def printPreReqs(preReqs, level, widthleft, widthright):
                preReqLength = len(preReqs)
                for i in range(preReqLength):
                    width_center = widthleft + (widthright - widthleft) * (2 * i + 1) // (2 * preReqLength)
                    temp = []
                    temp.append(self.display.create_window(width_center, (self.h // 2) + scale * level,
                                                          window = tkinter.Button(self, text = preReqs[i].get_title(),
                                                          fg=self.colorForeground(level), bg =self.colorBackground(preReqs[i].get_title()),
                                                          command = self.OnButtonClick(preReqs[i]))))
                    if(level):
                        temp.append(self.display.create_line(width_center, (self.h // 2) + scale * level - self.sSize // 2, 
                                                             widthleft + (widthright - widthleft) // 2, self.h // 2 + scale * (level - 1) + self.sSize // 2))
                    self.coursePrereqRects.append(temp)
                    preReq2 = self.database.get_prereq_courses(preReqs[i].get_title())
                    if len(preReq2):
                        printPreReqs(preReq2, level + 1, widthleft + ((widthright - widthleft) * i) // len(preReqs), 
                                     widthleft + ((widthright - widthleft) * (i + 1)) // len(preReqs))
            printPreReqs([self.currentCourse], 0, 0,self.w//2)
    def colorBackground(self,classname):
        if classname in self.colorDict:
            return self.colorDict[classname]
        else:
            r = lambda: random.randint(128,255)
            self.colorDict[classname]=('#%02X%02X%02X' % (r(),r(),r()))
        return self.colorDict[classname]
    def colorForeground(self,level):
        if level:
            return "black"
        else:
            return "dark blue"
    def OnButtonClick(self, course):
        return lambda: self.printCourseTree(course)

if __name__ == "__main__":
    app = CmapsGui(None)
    app.title("Course Map")
    app.mainloop()
