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

        self.courseInfo = tkinter.Canvas(self, width = self.w // 2, height = self.h)
        self.courseInfo.grid(column = 1, row = 1)

    def OnCourseEntry(self, event):
        try:
            self.currentCourse = self.database.get_course(self.entryValue.get().upper())
        except KeyError:
            print("Invalid Course Title")
        if self.currentCourse:
            self.display.delete(self.courseRect)
            self.display.delete(self.courseText)
            self.courseRect = self.display.create_rectangle(self.w // 4 - self.sSize // 2, self.h // 2 - self.sSize // 2, self.w // 4 + self.sSize // 2, self.h // 2 + self.sSize // 2, fill = "white")
            self.courseText = self.display.create_text(self.w // 4, self.h // 2, text = self.currentCourse.get_title())
        

if __name__ == "__main__":
    app = CmapsGui(None)
    app.title("Course Map")
    app.mainloop()
