# MINIMALIST DESKTOP STOPWATCH 
# Core Functions: Start, Stop, Lap/Split, Reset, Resume, Save lap file

# Import libraries
from tkinter import *
import time
import keyboard, threading

class StopWatch(Frame):                                                            
    def __init__(self, parent=None, **kw):        
        Frame.__init__(self, parent, kw)
        self._start = 0.0        
        self._elapsedtime = 0.0
        self._running = 0
        self.timestr = StringVar()
        self.lap_time_box = 0
        self.widget()
        self.laps = [] 
        self.old_time = 0
        self.today = time.strftime("%d %b %Y %H-%M-%S", time.localtime())  

    # widget    
    def widget(self):       
        # Create a canvas
        my_canvas = Canvas(width = 800, height = 500, bg = "#273755", highlightthickness = 0)
        my_canvas.pack()

        Filename = Label(text='File name:', bg = "#273755", fg = "white", font = ("Lato",16,"bold"))
        Filename.place(x = 200, y = 455, width = 200, height = 40)

        self.file_name_box = Entry(bg = "#273755", fg = "white", font = ("Lato",12)) 
        self.file_name_box.place(x = 360, y = 460, width = 150, height = 30)
        
        clock = Label(textvariable=self.timestr, bg = "#273755", fg = "white", font = ("Lato",90,"bold"))
        self.time(self._elapsedtime)
        clock.place(x = 150,y = 120,width = 500,height = 90) 

        my_canvas.create_text(227,225, text = "MINUTES", fill = "white", anchor = "c", font = ("Lato",10)) 
        my_canvas.create_text(370,225, text = "SECONDS", fill = "white", anchor = "w", font = ("Lato",10))

        LapTime = Label(text='Lap Times',  bg = "#273755", fg = "white", font = ("Lato",20,"bold"),)
        LapTime.place(x = 200,y = 320,width = 400,height = 30)

        scrollbar = Scrollbar(orient=VERTICAL)
        self.lap_time_box = Listbox(selectmode=EXTENDED, height = 5, yscrollcommand = scrollbar.set, bg = "#273755", fg = "white", font = ("Lato", 12), border = 0)
        self.lap_time_box.place(x = 240,y = 350,width = 300,height = 100)
        scrollbar.config(command = self.lap_time_box.yview,highlightthickness=0)
        scrollbar.place(x = 255,y = 350,width = 300,height = 100)
        
        #digi_clock
        def digi_clock():
            Time = time.strftime("%I:%M %p")
            Date = time.strftime("%A %x")
    
            my_clock.config(text = Time)
            my_clock.after (1000, digi_clock)
            my_clock2.config(text = Date)
    
        def update():
            my_clock.config(text = "Text")

        # Clock configuration
        my_clock = Label(text = "", bg = "#273755", fg = "white", font = ("Lato", 24, "bold")) 
        my_clock.place(x = 330,y = 5,width = 150, height = 25) 
        my_clock2 = Label(text = " ", bg = "#273755", justify = "left", anchor = "w", fg = "white", font = ("Lato", 12))
        my_clock2.place(x = 343, y = 30,width = 150, height = 20) 

        digi_clock()

# Creating functions of the stopwatch
    # Updates time relative to time elapsed
    def update(self): 
        self._elapsedtime = time.time() - self._start
        self.time(self._elapsedtime)
        self._timer = self.after(50, self.update)
        
    # Setting time 
    def time(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        milliseconds = int((elap - minutes*60.0 - seconds)*100)                
        self.timestr.set('%02d:%02d.%02d' % (minutes, seconds, milliseconds))        
           
    # Start function
    def Start(self):                                   
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self.update()
            self._running = 1  
            
    # Stop function
    def Stop(self):                                    
        if self._running:
            self.after_cancel(self._timer)            
            self._elapsedtime = time.time() - self._start    
            self.time(self._elapsedtime)
            self._running = 0

    # Resume function
    def Resume(self):
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self.update()
            self._running = 1   

    # Reset Function
    def Reset(self):        
        self.lap_time_box.delete(0, END)                            
        self._start = time.time()
        self._elapsedtime = 0.0
        self.time(self._elapsedtime)
        self.laps = []
        self.old_time = 0
    
    # Setting lap-based time
    def create_LapTime(self, elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        milliseconds = int((elap - minutes*60.0 - seconds)*100)            
        return '%02d:%02d.%02d' % (minutes, seconds, milliseconds)
        
    #  Makes lap times
    def Lap_times(self):
        tempo = self._elapsedtime - self.old_time
        if self._running:
            self.laps.append(self.create_LapTime(tempo))
            self.lap_time_box.insert(END, self.laps[-1])
            self.lap_time_box.yview_moveto(1)
            self.old_time = self._elapsedtime
            time.sleep(0.1)

    #  Creates a file to save lap times
    def Save_LapFile(self):
        archives = str(self.file_name_box.get()) + ' - '
        with open(archives + self.today + '.txt', 'wb') as lapfile:
            for lap in self.laps:
                lapfile.write((bytes(str(lap) + '\n', 'utf-8')))  
def main():
    root = Tk()
    root.geometry("800x500")
    root.title("Stopwatch")
    root.configure(background=("#273755"))  
    root.resizable(0,0)     
    sw = StopWatch(root) 
    sw.pack(side=TOP)
    
    # Icon for Stopwatch
    Icon = PhotoImage(file = r"CODER_MONKS.png")
    root.iconphoto(False, Icon)
    
    # Images for buttons
    imagetest_1 = PhotoImage(file = r"START.png")
    imagetest_2 = PhotoImage(file = r"STOP.png")
    imagetest_3 = PhotoImage(file = r"LAP.png")
    imagetest_4 = PhotoImage(file = r"RESTART.png")
    imagetest_5 = PhotoImage(file = r"SAVE.png")

    # Resizing image to fit on button 
    photoimage_1 = imagetest_1.subsample(48,28)
    photoimage_2 = imagetest_2.subsample(48,28)
    photoimage_3 = imagetest_3.subsample(48,28)
    photoimage_4 = imagetest_4.subsample(48,28)
    photoimage_5 = imagetest_5.subsample(123,123)

    Start_Button = Button(image = photoimage_1, borderwidth = 0, command=sw.Start)
    Stop_Button = Button(image = photoimage_2, borderwidth = 0, command=sw.Stop)
    Lap_Button = Button(image = photoimage_3, borderwidth = 0, command=sw.Lap_times)
    Reset_Button = Button(image = photoimage_4, borderwidth = 0, command=sw.Reset)
    Save_Button = Button(image = photoimage_5, borderwidth = 0, command=sw.Save_LapFile)

    Start_Button.place(x = 210, y = 260, width = 70, height = 30)
    Stop_Button.place(x = 315, y = 260, width = 70, height = 30) 
    Lap_Button.place(x = 420, y = 260, width = 70, height = 30)
    Reset_Button.place(x = 525, y = 260, width = 70, height = 30)
    Save_Button.place(x = 520, y = 462, width = 25, height = 25)
    
# Hotkeys configuration
    def key_loop():      
        while True:
            if keyboard.is_pressed("spacebar"):
                sw.Start()
            elif keyboard.is_pressed("shift"):
                sw.Stop()
            elif keyboard.is_pressed("enter"):
                sw.Lap_times()
            elif keyboard.is_pressed("backspace"):
                sw.Reset()
            elif keyboard.is_pressed("ctrl + s"):
                sw.Save_LapFile()
            time.sleep(0.1)

    thread = threading.Thread(target = key_loop).start()
    root.mainloop() 

if __name__ == '__main__':
    main()
