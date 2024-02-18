import tkinter as tk

from PIL import ImageTk, Image
import numpy as np
import matplotlib.pyplot as plt

root = tk.Tk()


class MainWindow:
    __Title = "Hinter"
    __windowWidth = 500  # 窗口宽度
    __windowHeigth = 750  # 窗口高度
    POINT_WIDTH = 40
    POINT_HEIGHT = 40
    X_OFFSET = 40
    Y_OFFSET = 80
    PADDING = 3



    def __init__(self):
        self.photos = None
        root.title(self.__Title)
        self.createWindow(self.__windowWidth, self.__windowHeigth)
        root.minsize(460, 460)
        self.__addComponets()

    def createWindow(self, width, height):
        screenheight = root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (width, height, 0, (screenheight - height) / 2)
        print(size)
        root.geometry(size)

    def __addComponets(self):
        # 地图尺寸、颜色
        self.canvas = tk.Canvas(root, bg='lightblue', width=450, height=700)
        # 插入文字
        # self.text = self.canvas.create_text(100, 320, anchor='nw', text='哆啦A梦连连看', fill="white", fon=('华文彩云', 30))
        self.canvas.pack(side=tk.TOP, pady=5)
        self.canvas.bind('<Button-1>')  # , self.clickCanvas)

    def draw_square(self, square_list, rows, cols):
        LEFT = self.X_OFFSET
        TOP = self.Y_OFFSET
        BOTTOM = self.Y_OFFSET + rows * self.POINT_HEIGHT
        RIGHT = self.X_OFFSET + cols * self.POINT_WIDTH
        for i in range(rows + 1):
            y = TOP + i * self.POINT_HEIGHT
            self.canvas.create_line(LEFT, y, RIGHT, y, fill='blue')

        for i in range(cols + 1):
            x = LEFT + i * self.POINT_WIDTH
            self.canvas.create_line(x, TOP, x, BOTTOM, fill='red')

        self.photos = [[None for _ in range(cols)] for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                x = LEFT + j * self.POINT_WIDTH + self.PADDING
                y = TOP + i * self.POINT_HEIGHT + self.PADDING
                idx = j * 10 + i
                image = Image.fromarray(np.array(square_list[idx]))
                # plt.imshow(image)
                # plt.show()
                self.photos[i][j] = ImageTk.PhotoImage(image)

                self.canvas.create_image((x, y), image=self.photos[i][j], anchor='nw', tags='im%d%d' % (i, j))



