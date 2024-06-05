import tkinter as tk

root = tk.Tk()

# Create a Text widget
text_widget = tk.Text(root, height=5, width=40)
text_widget.pack(side=tk.LEFT)

# Create a Scrollbar and associate it with the Text widget
scroll_bar = tk.Scrollbar(root, command=text_widget.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

# Link the movement of the Scrollbar with the Text widget
text_widget.config(yscrollcommand=scroll_bar.set)

root.mainloop()
