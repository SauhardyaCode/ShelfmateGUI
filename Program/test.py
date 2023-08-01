from tkinter import *

from tkinter import ttk



root = Tk()

root.title('Full Window Scrolling X Y Scrollbar Example')

root.state("zoomed")

# Create A Canvas

my_canvas = Canvas(root)

my_canvas.pack(side=LEFT,fill=BOTH,expand=1)



# Add A Scrollbars to Canvas

y_scrollbar = ttk.Scrollbar(root,orient=VERTICAL,command=my_canvas.yview)
y_scrollbar.pack(side=RIGHT,fill=Y)



# Configure the canvas

my_canvas.configure(yscrollcommand=y_scrollbar.set)

my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL)))

def _on_mousewheel(event):
    my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

my_canvas.bind_all("<MouseWheel>", _on_mousewheel)




# Create Another Frame INSIDE the Canvas

second_frame = Frame(my_canvas)

for i in range(100):
    b = Button(second_frame, text=f"Button {i+1}")
    b.grid(row=i, column=0)



# Add that New Frame a Window In The Canvas

my_canvas.create_window((0,0),window= second_frame, anchor="nw")

root.mainloop()