from screeninfo import get_monitors
import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "Settings.ui"


class SettingsApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)

        self.radioVar = tk.StringVar()  # used to get the 'value' property of a tkinter.Radiobutton
        self.radioVar.set(True)

        self.labelframe1 = ttk.Labelframe(self.toplevel1)
        self.fullscreen = ttk.Radiobutton(self.labelframe1)
        self.fullscreen.configure(text='Fullscreen', variable=self.radioVar, value=True)
        self.fullscreen.pack(anchor='w', side='top')
        self.windowed = ttk.Radiobutton(self.labelframe1)
        self.windowed.configure(text='Window', variable=self.radioVar, value=False)
        self.windowed.pack(anchor='w', side='top')
        self.labelframe1.configure(height='200', text='Window mode', width='200')
        self.labelframe1.pack(anchor='nw', ipadx='10', ipady='10', padx='10', pady='10', side='top')
        self.label1 = ttk.Label(self.toplevel1)
        self.label1.configure(text='Monitor')
        self.label1.pack(anchor='w', padx='10', side='top')

        self.selected_monitor = tk.StringVar()
        self.Monitorbox = ttk.Combobox(self.toplevel1, textvariable=self.selected_monitor)
        self.Monitorbox.pack(anchor='w', padx='10', side='top')

        self.monitor_list = get_monitors()
        for idx, m in enumerate(self.monitor_list):
            m.name = "Display{num}".format(num=idx+1)
            self.Monitorbox['values'] += str(m.name)
        self.Monitorbox.current(0)
        self.Monitorbox['state'] = 'readonly'


        self.label2 = ttk.Label(self.toplevel1)
        self.label2.configure(text='Webcam')
        self.label2.pack(anchor='w', padx='10', side='top')
        self.Webcambox = ttk.Combobox(self.toplevel1)
        self.Webcambox.pack(anchor='w', padx='10', side='top')
        self.Hand = ttk.Button(self.toplevel1)
        self.Hand.configure(text='Calibrate hand')
        self.Hand.pack(anchor='w', padx='10', pady='10', side='top')
        self.Hand.configure(command=self.calibrate_hands)
        self.Corner = ttk.Button(self.toplevel1)
        self.Corner.configure(text='Calibrate corners')
        self.Corner.pack(anchor='w', padx='10', pady='10', side='top')
        self.Corner.configure(command=self.calibrate_corners)
        self.Cancel = ttk.Button(self.toplevel1)
        self.Cancel.configure(text='Cancel')
        self.Cancel.pack(anchor='se', padx='10', pady='10', side='right')
        self.Cancel.configure(command=self.cancle)
        self.OK = ttk.Button(self.toplevel1)
        self.OK.configure(text='OK')
        self.OK.pack(anchor='se', padx='10', pady='10', side='right')
        self.OK.configure(command=self.save)
        self.toplevel1.configure(borderwidth='2', height='200', width='200')
        self.toplevel1.geometry('352x352')
        self.toplevel1.title('Settings')

        # Main widget
        self.mainwindow = self.toplevel1


    def run(self):
        self.mainwindow.mainloop()

    def calibrate_hands(self):
        pass

    def calibrate_corners(self):
        pass

    def cancle(self):
        pass

    def save(self):
        print("is fullscreen: " + self.radioVar.get())
        for m in self.monitor_list:
            if m.name == self.selected_monitor.get():
                print(m)

def runsettings():
    app = SettingsApp()
    app.run()

