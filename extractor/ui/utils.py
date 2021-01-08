def center_window(widget, width: int, height: int):
    x = (widget.winfo_screenwidth() - width) // 2
    y = (widget.winfo_screenheight() - height) // 2
    widget.geometry(f'{width}x{height}+{x}+{y}')
