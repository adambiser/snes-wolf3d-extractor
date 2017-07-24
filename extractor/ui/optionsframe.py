import Tkinter as tk

class OptionsFrame(tk.LabelFrame):
    COLUMNS = 3
    def __init__(self, parent, settings, **options):
        tk.LabelFrame.__init__(self, parent, **options)
        self.config(text='Export Settings')
        self.parent = parent
        self.settings = settings
        # Add widgets.
        keys = settings.export.keys()
        keys.sort()
        row = 0
        col = 0
        for key in keys:
            tk.Checkbutton(self,
                           text=key,
                           variable=self.settings.export[key]
                           ).grid(row=row,
                                  column=col,
                                  sticky=tk.W
                                  )
            col += 1
            if col == OptionsFrame.COLUMNS:
                row += 1
                col = 0
        for col in range(OptionsFrame.COLUMNS):
            tk.Grid.columnconfigure(self, col, weight=1)
