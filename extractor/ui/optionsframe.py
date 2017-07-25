import Tkinter as tk

class OptionsFrame(tk.LabelFrame):
    COLUMNS = 3
    def __init__(self, parent, settings, **options):
        tk.LabelFrame.__init__(self, parent, **options)
        self.config(text='Export Options',
                    padx=5,
                    pady=5)
        self.parent = parent
        # Add widgets.
        tk.Checkbutton(self,
                       text='Export to subfolder named after ROM',
                       variable=settings.export_to_subfolder,
                       ).pack(anchor=tk.NW,
                              )
        tk.Checkbutton(self,
                       text='Combine maps into single file',
                       variable=settings.combine_maps,
                       ).pack(anchor=tk.NW,
                              )
        subframe = tk.LabelFrame(self, text='ROM Entry Types')
        subframe.pack(fill=tk.X,
                      )
        keys = settings.export.keys()
        keys.sort()
        row = 0
        col = 0
        for key in keys:
            tk.Checkbutton(subframe,
                           text=key,
                           variable=settings.export[key],
                           ).grid(row=row,
                                  column=col,
                                  sticky=tk.W,
                                  )
            col += 1
            if col == OptionsFrame.COLUMNS:
                row += 1
                col = 0
        for col in range(OptionsFrame.COLUMNS):
            tk.Grid.columnconfigure(subframe, col, weight=1, uniform='a')
