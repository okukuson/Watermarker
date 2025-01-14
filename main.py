import tkinter as tk
from tkinter import filedialog, colorchooser
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont


class engine:
    def __init__(self):
        self.img = None
        self.text = None
        self.watermarked_image = None
        self.x_axis = 5
        self.y_axis = 150
        self.font = 24
        self.color = (255,0,0)
        self.file_types = [('Picture file', '.jpeg'),
                           ('Picture file', '.jpg'),
                           ('Picture file', '.PNG'), ]

    # Function to open background image
    def open_file(self):
        file = filedialog.askopenfilename(title="Select file", filetypes=self.file_types)
        raw_image = Image.open(file)
        self.img = raw_image.resize((400, 400))
        backgroundpaper = ImageTk.PhotoImage(self.img)
        display_canvas.create_image(200, 200, image=backgroundpaper)
        display_canvas.image = backgroundpaper

    # Save the watermarked image
    def save_image(self):
        print('success')
        file = filedialog.asksaveasfilename(filetypes=self.file_types, defaultextension=self.file_types)
        print(file)
        self.watermarked_image.save(file)

    # Function to rotate the background image
    def rotate(self):
        self.img = self.img.transpose(Image.Transpose.ROTATE_90)
        backgroundpaper = ImageTk.PhotoImage(self.img)
        display_canvas.create_image(200, 200, image=backgroundpaper)
        display_canvas.image = backgroundpaper

    # Function to impose text on image
    def impose_text(self, text, text_font):
        self.text = text.get()
        self.font = text_font.get()
        self.watermark_text()

    # Spreads the text amongs multiple lines if the text is long
    def text_formatter(self, im):
        text_str = self.text
        text_list = text_str.split()
        out_put = []
        line = ''
        for word in text_list:
            line = line + word + ' '
            line_size = im.textlength(line, font_size=50)
            if line_size >= 350:
                if line_size < 370:
                    out_put.append(line)
                    line = ''
                elif line_size > 370:
                    rearrange = line.split()
                    new_start = rearrange.pop(-1)
                    out_put.append(' '.join(rearrange))
                    line = f'{new_start} '
            if word == text_list[-1]:
                out_put.append(line)
        return "\n".join(out_put)

    # writes the text on the image file
    def watermark_text(self):
        self.watermarked_image = self.img.copy()
        im = ImageDraw.Draw(self.watermarked_image)
        # self.font = text_font.get()
        water_text = self.text_formatter(im)
        im.text((self.x_axis,self.y_axis), water_text, self.color, font_size=self.font)
        backgroundpaper = ImageTk.PhotoImage(self.watermarked_image)
        display_canvas.create_image(200, 200, image=backgroundpaper)
        display_canvas.image = backgroundpaper

    # Control the watermark position
    def move_vertical(self, move):
        self.x_axis += move
        self.watermark_text()

    def move_horizontal(self, move):
        self.y_axis += move
        self.watermark_text()



        # if total_xter > max_character:
        #     x = 0
        #     if total_xter[:(max_character - x)].endswith(' '):

    # Color chooser function
    def select_color(self):
        color_code = colorchooser.askcolor(title='Choose color')
        self.color = color_code[0]
        print(color_code)




eng = engine()
root = tk.Tk()

watermark_text = tk.StringVar()
text_font =tk.IntVar(value=24)


# Open and save button
open_button = ttk.Button(root, text='Open', command=eng.open_file)
open_button.grid(row=0, column=0)
save_button = ttk.Button(root, text='Save', command=eng.save_image)
save_button.grid(row=0, column=12)

# Display canvas
display_canvas= tk.Canvas(root,bg='white', width=400, height=400)
display_canvas.grid(row=1, column=1, columnspan=10)

# Text watermark widgets
ttk.Label(root, text='Watermark Text').grid(row=2, column=0)

watermark_text = ttk.Entry(root, text='Watermark Text', width=60, textvariable=watermark_text)
watermark_text.grid(row=2, column=1, columnspan=10)
ttk.Button(root, text='Apply Text', command=lambda: eng.impose_text(watermark_text,text_font)).grid(row=2, column=11)

rotate_button = ttk.Button(root, text='Rotate', command=eng.rotate)
rotate_button.grid(row=4, column=1)

# text color and font configuration widgets
font_frame = ttk.Frame(root).grid(row=4, column=2)
ttk.Label(font_frame, text='font').grid(row=4, column=2, sticky='E')
ttk.Entry(font_frame, width=5, textvariable=text_font).grid(row=4, column=3, sticky='W')
color_button = ttk.Button(root, text='Color', command=eng.select_color)
color_button.grid(row=4, column=9)

# watermark positioning widgets
position = ttk.Label(root, text='Watermark Position')
position.grid(row=5, column=0)

button = ttk.Button(root, text='Up', command=lambda: eng.move_horizontal(-10))
button.grid(row=6, column=0, rowspan=3)

button = ttk.Button(root, text='Down', command=lambda: eng.move_horizontal(+10))
button.grid(row=6, column=1, rowspan=3)

button = ttk.Button(root, text='Left', command=lambda: eng.move_vertical(-10))
button.grid(row=6, column=2, rowspan=3)

button = ttk.Button(root, text='Right', command=lambda: eng.move_vertical(10))
button.grid(row=6, column=3, rowspan=3)



root.mainloop()

