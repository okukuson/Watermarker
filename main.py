import tkinter as tk
from tkinter import filedialog
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

    # Function to open background image
    def open_file(self):
        file = filedialog.askopenfilename(title="Select file", filetypes=[('Picture file', '.jpeg'),
                                                                          ('Picture file', '.jpg'),
                                                                          ('Picture file', '.PNG'), ])
        raw_image = Image.open(file)
        self.img = raw_image.resize((400, 400))
        backgroundpaper = ImageTk.PhotoImage(self.img)
        display_canvas.create_image(200, 200, image=backgroundpaper)
        display_canvas.image = backgroundpaper

    # Function to rotate the background image
    def rotate(self):
        self.img = self.img.transpose(Image.Transpose.ROTATE_90)
        backgroundpaper = ImageTk.PhotoImage(self.img)
        display_canvas.create_image(200, 200, image=backgroundpaper)
        display_canvas.image = backgroundpaper

    # Function to impose text on image
    def impose_text(self, text):
        self.text = text.get()
        self.watermark_text()

    def text_formatter(self, im):
        text_str = self.text
        text_list = text_str.split()
        print(text_list)
        out_put = []
        line = ''
        # while im.textlength()
        for word in text_list:
            line = line + word + ' '
            print(line)
            line_size = im.textlength(line, font_size=50)
            print(line_size)
            if line_size >= 350:
                print('greater')
                if line_size < 370:
                    out_put.append(line)
                    print('less than 370')
                    line = ''
                elif line_size > 370:
                    rearrange = line.split()
                    new_start = rearrange.pop(-1)
                    out_put.append(' '.join(rearrange))
                    print(f'rearrange {" ".join(rearrange)}')
                    line = f'{new_start} '
            if word == text_list[-1]:
                out_put.append(line)
        print(out_put)
        print("\n".join(out_put))
        return "\n".join(out_put)


    def watermark_text(self):
        self.watermarked_image = self.img.copy()
        # self.watermarked_image.show()
        im = ImageDraw.Draw(self.watermarked_image)
        # myfont = ImageFont.truetype(30)
        water_text = self.text_formatter(im)
        im.text((self.x_axis,self.y_axis), water_text, (255,0,0), font_size=50)
        # print(im.textlength(self.text, font_size=50))
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




eng = engine()
root = tk.Tk()

watermark_text = tk.StringVar()

# Open and close button
open_button = ttk.Button(root, text='Open', command=eng.open_file)
open_button.grid(row=0, column=0)
close_button = ttk.Button(root, text='Save')
close_button.grid(row=0, column=12)

# Display canvas
display_canvas= tk.Canvas(root,bg='white', width=400, height=400)
display_canvas.grid(row=1, column=1, columnspan=10)

# Text watermark widgets
ttk.Label(root, text='Watermark Text').grid(row=2, column=0)

watermark_text = ttk.Entry(root, text='Watermark Text', width=60, textvariable=watermark_text)
watermark_text.grid(row=2, column=1, columnspan=10)
ttk.Button(root, text='Apply Text', command=lambda: eng.impose_text(watermark_text)).grid(row=2, column=11)

rotate_button = ttk.Button(root, text='Rotate', command=eng.rotate)
rotate_button.grid(row=4, column=1)

delete_button = ttk.Button(root, text='Delete')
delete_button.grid(row=4, column=9)

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

