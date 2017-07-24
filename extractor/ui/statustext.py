import Tkinter as tk

class StatusText(tk.LabelFrame):
    def __init__(self, parent, *args, **kwargs):
        tk.LabelFrame.__init__(self, parent, *args, **kwargs)
        self.config(text='Status')
        scrollbar = tk.Scrollbar(self,
                                 orient=tk.VERTICAL,
                                 )
        self.text = tk.Text(self,
                            state=tk.DISABLED,
                            yscrollcommand=scrollbar.set,
                            )
        scrollbar.config(command=self.text.yview)
        scrollbar.pack(side=tk.RIGHT,
                       fill=tk.Y,
                       padx=(0,5),
                       pady=5,
                       )
        self.text.pack(side=tk.LEFT,
                       fill=tk.BOTH,
                       expand=1,
                       padx=(5,0),
                       pady=5,
                       )

    def appendline(self, chars):
        if self.text.get('1.0', 'end-1c'):
            chars = '\n' + chars
        self.insert(tk.END, chars)
        
    def insert(self, index, chars, *args):
        self.text.config(state=tk.NORMAL)
        self.text.insert(index, chars, *args)
        self.text.config(state=tk.DISABLED)
        self.text.see(tk.END)
