from screeninfo import get_monitors, Monitor
import tkinter as tk
import tkinter.ttk as ttk
from Camera import Camera


class Settings:
    def __init__(self, monitor=Monitor(width=640, height=360, x=0, y=0), fullscreen=1, camera=0):
        self.monitor: Monitor = monitor
        self.isFullscreen = fullscreen
        self.camera = camera


class SettingsApp:
    def __init__(self, master=None):
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.appliedSettings = Settings()
        # radio button stuff
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


        # monitor stuff
        self.label1 = ttk.Label(self.toplevel1)
        self.label1.configure(text='Monitor')
        self.label1.pack(anchor='w', padx='10', side='top')
        self.selected_monitor = tk.StringVar()
        self.Monitorbox = ttk.Combobox(self.toplevel1, textvariable=self.selected_monitor)
        self.Monitorbox.pack(anchor='w', padx='10', side='top')
        self.monitor_list = {
        }
        for idx, m in enumerate(get_monitors()):
            self.monitor_list["Display{num}".format(num=idx + 1)] = m
        self.Monitorbox['values'] = list(self.monitor_list.keys())
        self.Monitorbox.current(0)
        self.Monitorbox['state'] = 'readonly'

        # webcam stuff
        self.active_cams = Camera.returnCameraIndexes()
        self.selected_cam = tk.StringVar()

        self.label2 = ttk.Label(self.toplevel1)
        self.label2.configure(text='Webcam')
        self.label2.pack(anchor='w', padx='10', side='top')
        self.Webcambox = ttk.Combobox(self.toplevel1, textvariable=self.selected_cam)
        self.Webcambox.pack(anchor='w', padx='10', side='top')
        self.Webcambox['values'] = self.active_cams
        self.Webcambox.current(0)
        self.Webcambox['state'] = 'readonly'

        # calibrate hand stuff
        self.Hand = ttk.Button(self.toplevel1)
        self.Hand.configure(text='Calibrate hand')
        self.Hand.pack(anchor='w', padx='10', pady='10', side='top')
        self.Hand.configure(command=self.calibrate_hands)

        # calibrate corners stuff
        self.Corner = ttk.Button(self.toplevel1)
        self.Corner.configure(text='Calibrate corners')
        self.Corner.pack(anchor='w', padx='10', pady='10', side='top')
        self.Corner.configure(command=self.calibrate_corners)

        # cancel button stuff
        self.Cancel = ttk.Button(self.toplevel1)
        self.Cancel.configure(text='Cancel')
        self.Cancel.pack(anchor='se', padx='10', pady='10', side='right')
        self.Cancel.configure(command=self.cancel)

        # ok button stuff
        self.OK = ttk.Button(self.toplevel1)
        self.OK.configure(text='OK')
        self.OK.pack(anchor='se', padx='10', pady='10', side='right')
        self.OK.configure(command=self.save)

        # main widget stuff
        self.toplevel1.configure(borderwidth='2', height='200', width='200')
        self.toplevel1.geometry('352x352')
        self.toplevel1.title('Settings')

        # Main widget
        self.mainwindow = self.toplevel1

    def run(self) -> Settings:
        self.mainwindow.mainloop()

        return self.appliedSettings

    def calibrate_hands(self):
        pass

    def calibrate_corners(self):
        pass

    def cancel(self):
        self.toplevel1.destroy()

    def save(self):
        self.appliedSettings.monitor = self.monitor_list[self.selected_monitor.get()]
        self.appliedSettings.isFullscreen = int(self.radioVar.get())
        self.appliedSettings.camera = int(self.selected_cam.get())
        if int(self.radioVar.get()) == 0:
            self.appliedSettings.monitor.width = 640
            self.appliedSettings.monitor.height = 360

        self.toplevel1.destroy()


def runsettings() -> Settings:
    app = SettingsApp()
    return app.run()
