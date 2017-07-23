import Tkinter as tk

class OptionsFrame(tk.LabelFrame):
    def __init__(self, parent, settings, **options): # *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, **options) #*args, **kwargs)
##        self.config(borderwidth=1
        self.config(text='Export Settings')
        self.parent = parent
        self.settings = settings
        # Widget creation.
        self.checkbuttons = []
        keys = settings.export.keys()
        keys.sort()
        row = 0
        col = 0
        for k in keys:
            chk = tk.Checkbutton(self, text=k, variable=self.settings.export[k])
            self.checkbuttons.append(chk)
            self.checkbuttons[-1].grid(row=row, column=col, sticky=tk.W)
            col += 1
            if col == 3:
                row += 1
                col = 0
        for x in range(3):
            tk.Grid.columnconfigure(self, x, weight=1)
