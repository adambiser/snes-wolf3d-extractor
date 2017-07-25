def center_window(widget, width, height):
    x = (widget.winfo_screenwidth() - width) / 2
    y = (widget.winfo_screenheight() - height) / 2
    widget.geometry('%dx%d+%d+%d' % (width, height, x, y))

