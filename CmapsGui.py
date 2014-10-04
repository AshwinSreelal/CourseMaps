import tkinter, database, course

class CmapsGui(tkinter.Tk):
    def __init__(self, parent):
        tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.w, self.h, self.sSize = 1280, 720, 80
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
        self.courseEntry.grid(column = 0, row = 0, columnspan = 2, sticky = "EW")
        self.courseEntry.bind("<Return>", self.OnCourseEntry)

        self.display = tkinter.Canvas(self, width = self.w // 2, height = self.h)
        self.display.grid(column = 0, row = 1)
        self.display.create_line(self.w // 2, 0, self.w // 2, self.h)
        self.courseRect = self.display.create_rectangle(0, 0, 0, 0, fill = "white")
        self.courseText = self.display.create_text(0, 0, text = "")
        self.coursePrereqRects = []

        self.courseInfo = tkinter.Canvas(self, width = self.w // 2, height = self.h)
        self.courseInfo.grid(column = 1, row = 1)
        self.infoText = self.courseInfo.create_text(0, 0, text = "")

    def OnCourseEntry(self, event):
        try:
            self.currentCourse = self.database.get_course(self.entryValue.get().upper())
        except KeyError:
            print("Invalid Course Title")
        if self.currentCourse:
            self.display.delete(self.courseRect)
            self.display.delete(self.courseText)
            self.courseInfo.delete(self.infoText)
            for prereq in self.coursePrereqRects:
                for icon in prereq:
                    self.display.delete(icon) 
            x1, y1, x2, y2 = self.centerToCorners(self.w // 4, self.h // 2, self.sSize)
            self.courseRect = self.display.create_rectangle(x1, y1, x2, y2, fill = "white")
            self.courseText = self.display.create_text(self.w // 4, self.h // 2, text = self.currentCourse.get_title())
            self.infoText = self.courseInfo.create_text(100, 100, anchor = "nw", 
                                                        text = "Units: " + str(self.currentCourse.get_num_units()) + "\n\n" + self.currentCourse.get_courseinfo(), 
                                                        width = self.w // 2 - 200)
            preReqs = self.database.get_prereq_courses(self.currentCourse.get_title())
            preReqLength = len(preReqs)
            for i in range(preReqLength):
                width_center = (self.w * (2 * i + 1)) / (4 * preReqLength)
                temp = []
                x1, y1, x2, y2 = self.centerToCorners(width_center, (self.h * 3) // 4, self.sSize)
                temp.append(self.display.create_rectangle(x1, y1, x2, y2, fill = "white"))
                temp.append(self.display.create_text(width_center, (self.h * 3) // 4, text = preReqs[i].get_title()))
                temp.append(self.display.create_line(width_center, (self.h * 3) // 4 - self.sSize // 2, self.w // 4, self.h // 2 + self.sSize // 2))
                self.coursePrereqRects.append(temp)

                
        
    def centerToCorners(self, x, y, sideLength):
        return x - sideLength // 2, y - sideLength // 2, x + sideLength // 2, y + sideLength // 2

if __name__ == "__main__":
    app = CmapsGui(None)
    app.title("Course Map")
    app.mainloop()
