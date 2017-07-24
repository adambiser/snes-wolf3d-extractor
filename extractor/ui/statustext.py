import Tkinter as tk

class StatusText(tk.LabelFrame):
    def __init__(self, parent, **options):
        tk.LabelFrame.__init__(self, parent, **options)
        self.config(text='Status')
        self.parent = parent
        scrollbar = tk.Scrollbar(self,
                                 orient=tk.VERTICAL,
                                 )
        self.textbox = tk.Text(self,
                               state=tk.DISABLED,
                               height=1,
                               yscrollcommand=scrollbar.set,
                               )
        scrollbar.config(command=self.textbox.yview)
        scrollbar.pack(anchor=tk.NE,
                       side=tk.RIGHT,
                       fill=tk.Y,
                       padx=(0,5),
                       pady=5,
                       )
        self.textbox.pack(anchor=tk.NW,
                       side=tk.LEFT,
                       fill=tk.BOTH,
                       expand=1,
                       padx=(5,0),
                       pady=5,
                       )

    def appendline(self, chars):
        if self.textbox.get('1.0', 'end-1c'):
            chars = '\n' + chars
        self.textbox.config(state=tk.NORMAL)
        self.textbox.insert(tk.END, chars)
        self.textbox.config(state=tk.DISABLED)
        self.textbox.see(tk.END)
