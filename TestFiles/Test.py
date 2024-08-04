"""from tkinter import Tk, Canvas, NW
from PIL import Image, ImageTk
from ctypes import windll





win = Tk()

photoimage = ImageTk.PhotoImage(Image.open(f"White_Knight.png"))

photoimage2 = ImageTk.PhotoImage(Image.open(f"White_Knight.png"))

win.config(bg="#000000")

width, height = photoimage.width(), photoimage.height()
canvas = Canvas(win)
canvas.pack()

canvas.create_image(0, 0, image=photoimage, anchor=NW)
canvas.create_image(0, 0, image=photoimage2)

win.mainloop()"""


"""import tkinter as tk
from tkinter import font

root = tk.Tk()
root.geometry("400x300")

# Get a list of all available fonts
available_fonts = list(font.families())

# Display the available fonts in a Listbox
listbox = tk.Listbox(root)
listbox.pack(fill=tk.BOTH, expand=True)

for f in available_fonts:
    print(f)

"""



"""import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Selectable Text")

# Create a canvas
manga_Canvas = tk.Canvas(root, background="#2E2E2E")
manga_Canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Example data
manga_name_text = "This is a very long manga name that should wrap to the next line if it exceeds the width of the label"

# Create a Text widget with read-only state
manga_name = tk.Text(
    manga_Canvas,
    background="#373737",
    fg="#0075A4",
    highlightbackground="#0B0B0B",
    highlightthickness=3,
    wrap=tk.WORD,
    width=50,
    height=5
)

# Insert the text into the Text widget
manga_name.insert(tk.END, manga_name_text)
manga_name.config(state=tk.DISABLED)  # Make the Text widget read-only

# Place the Text widget at a relative position
manga_name.place(relx=0.5, rely=0.5, anchor="center")

# Function to get the relative coordinates of the Text widget
def get_text_rely():
    place_info = manga_name.place_info()
    relx = place_info.get("relx")
    rely = place_info.get("rely")
    print(f"Text widget relx: {relx}, rely: {rely}")

# Create a button to trigger the function and get the rely value
get_rely_button = tk.Button(root, text="Get Text rely", command=get_text_rely)
get_rely_button.pack(pady=10)

# Run the application
root.mainloop()"""


"""def split_array(array):
    sub_arrays = [array[i:i+3] for i in range(0, len(array), 3)]
    return sub_arrays

# Example usage:
array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
result = split_array(array)
print(result)"""


"""from tkinter import *

root = Tk()

fr = Frame(root)
fr.grid(row=0, column=0, sticky=N)
fr2 = Frame(root, height=34)
fr2.grid(row=0, column=1, sticky=N)

text_area = Listbox(fr2, width = 28, height= 34)
text_area.grid(row=0, column=0, rowspan=20)

sb = Scrollbar(fr2, command=text_area.yview)
sb.grid(column=1, row=0, sticky="ns", rowspan=20)

text_area.config(font = ("Courier New", 12), yscrollcommand = sb.set)

for i in range(100):
    text_area.insert("end", "item #{}".format(i))

root.mainloop()"""

"""import tkinter as tk

class CenteredListbox(tk.Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.listbox_frame = tk.Frame(self)
        self.listbox_frame.pack(fill=tk.BOTH, expand=True)
        self.listbox = tk.Listbox(self.listbox_frame, relief=tk.FLAT, activestyle='none')
        self.listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        self.vsb = tk.Scrollbar(self.listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=self.vsb.set)

        # Bind the selection event
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

    def insert(self, index, element, colors):
        self.listbox.insert(index, element)
        self.listbox.itemconfig(index, {'background': colors[index % 2], 'selectbackground': colors[index % 2]})
        self.listbox.bind('<Configure>', self.center_items)

    def center_items(self, event=None):
        for idx in range(self.listbox.size()):
            item_text = self.listbox.get(idx)
            item_width = self.listbox.bbox(idx)[2]
            listbox_width = self.listbox.winfo_width()
            padx = (listbox_width - item_width) // 2
            self.listbox.itemconfig(idx, {'padx': padx})

    def on_select(self, event):
        # Get the index of the selected item
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_index = selected_index[0]
            selected_item = self.listbox.get(selected_index)
            print(f'Selected item: {selected_item}')

root = tk.Tk()
root.geometry("400x400")

# Example usage
Chapters = ["Chapter 1", "Chapter 2", "Chapter 3"]
Colors = ["#f0f0f0", "#e0e0e0"]

centered_listbox = CenteredListbox(root, bg="white")
centered_listbox.pack(fill=tk.BOTH, expand=True)

for index, Chapter in enumerate(Chapters):
    centered_listbox.insert(index, Chapter, Colors)

root.mainloop()"""

"""import tkinter as tk

class CustomListbox(tk.Listbox):
    def __init__(self, master, widget_info, **kwargs):
        super().__init__(master, **kwargs)
        self.widget_info = widget_info
        self.bind('<Motion>', self.on_hover)

    def on_hover(self, event):
        content_box_height_size = self.widget_info["Size"][1] - 10
        number_of_elements = self.widget_info["NumberOfChapter"]
        number_of_displayed_elements = content_box_height_size // 19
        number_of_elements_behind = self.index('@0,0')
        hovered_over_element_index = ((event.y - 5) // 19) + number_of_elements_behind
        
        if 0 <= hovered_over_element_index < number_of_elements:
            for i in range(number_of_elements):
                self.itemconfig(i, background=self.widget_info["ElementColors"][i % 2])
            self.itemconfig(hovered_over_element_index, background="#9CDCFE")
            self.widget_info["HoveredIndex"] = hovered_over_element_index


root = tk.Tk()
root.geometry("400x400")

widget_info = {
    "Size": (0, 0),
    "NumberOfChapter": 3,
    "ElementColors": ["#000000", "#1F1F1F"],
    "HoveredIndex": None
}

custom_listbox = CustomListbox(root, widget_info, bg="white")
custom_listbox.pack(fill=tk.BOTH, expand=True)

chapters = ["Chapter 1", "Chapter 2", "Chapter 3"]
for index, chapter in enumerate(chapters):
    custom_listbox.insert(index, chapter)

widget_info["Size"] = (custom_listbox.winfo_width(), custom_listbox.winfo_height())
widget_info["NumberOfChapter"] = custom_listbox.size()

root.mainloop()"""


"""import tkinter as tk

class CenteredListbox(tk.Listbox):
    def __init__(self, master, widget_info, **kwargs):
        super().__init__(master, **kwargs)
        self.widget_info = widget_info
        self.bind('<Motion>', self.on_hover)
        self.bind('<Configure>', self.center_items)

    def center_items(self, event=None):
        for idx in range(self.size()):
            item_text = self.get(idx)
            item_width = self.bbox(idx)[2]
            listbox_width = self.winfo_width()
            padx = (listbox_width - item_width) // 2
            self.itemconfig(idx, {'padx': padx})

    def on_hover(self, event):
        content_box_height_size = self.widget_info["Size"][1] - 10
        number_of_elements = self.widget_info["NumberOfChapter"]
        number_of_displayed_elements = content_box_height_size // 19
        number_of_elements_behind = self.index('@0,0')
        hovered_over_element_index = ((event.y - 5) // 19) + number_of_elements_behind

        if 0 <= hovered_over_element_index < number_of_elements:
            for i in range(number_of_elements):
                self.itemconfig(i, background=self.widget_info["ElementColors"][i % 2])
            self.itemconfig(hovered_over_element_index, background="#9CDCFE")
            self.widget_info["HoveredIndex"] = hovered_over_element_index

            # Get the pixel size of the hovered element
            bbox = self.bbox(hovered_over_element_index)
            if bbox:
                item_width, item_height = bbox[2], bbox[3]
                print(f'Hovered over element index: {hovered_over_element_index}')
                print(f'Element size - Width: {item_width} px, Height: {item_height} px')


root = tk.Tk()
root.geometry("400x400")

widget_info = {
    "Size": (0, 0),
    "NumberOfChapter": 3,
    "ElementColors": ["#000000", "#1F1F1F"],
    "HoveredIndex": None
}

centered_listbox = CenteredListbox(root, widget_info, bg="white")
centered_listbox.pack(fill=tk.BOTH, expand=True)

chapters = ["Chapter 1", "Chapter 2", "Chapter 3"]
for index, chapter in enumerate(chapters):
    centered_listbox.insert(index, chapter)

widget_info["Size"] = (centered_listbox.winfo_width(), centered_listbox.winfo_height())
widget_info["NumberOfChapter"] = centered_listbox.size()

root.mainloop()
"""


import tkinter as tk

class CustomDropdownExample:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Multi-Column Drop-Down Example")

        # Create a button to open the custom drop-down
        self.button = tk.Button(root, text="Open Custom Menu", command=self.open_custom_menu)
        self.button.pack(pady=20)

    def open_custom_menu(self):
        # Create a custom drop-down menu using a Toplevel window
        menu = tk.Toplevel(self.root)
        menu.title("Custom Menu")

        # Remove the window decorations
        menu.overrideredirect(False)
        
        # Define options and layout
        options = [

        ]
        for i in range(300):
            options.append(i)
        
        num_columns = 8
        for i in range(len(options)):
            row = i // num_columns
            column = i % num_columns
            tk.Button(menu, text=options[i], command=lambda opt=options[i]: self.on_option_select(opt)).grid(row=row, column=column, padx=5, pady=5)
        
        # Center the custom menu on the parent window
        self.center_window(menu)

        # Add a close button to the custom menu
        close_button = tk.Button(menu, text="Close", command=menu.destroy)
        close_button.grid(row=(len(options) // num_columns) + 1, column=0, columnspan=num_columns, pady=5)

    def on_option_select(self, option):
        # Handle option selection
        print(f"Selected option: {option}")

    def center_window(self, window):
        # Center the Toplevel window on the parent window
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

# Create the main window
root = tk.Tk()
app = CustomDropdownExample(root)

# Run the application
root.mainloop()