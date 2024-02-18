import tkinter as tk

root = tk.Tk()


class MainWindow:
    __Title = "Hinter"
    __windowWidth = 500  # 窗口宽度
    __windowHeigth = 750  # 窗口高度
    __icons = []
    __gameSize = 10  # 游戏尺寸
    __iconKind = __gameSize * __gameSize / 4  # 小图片种类数量
    __iconWidth = 40  # 小图片宽度
    __iconHeight = 40  # 小图片高度
    __map = []  # 游戏地图
    __delta = 25

    def __init__(self):
        root.title(self.__Title)
        self.createWindow(self.__windowWidth, self.__windowHeigth)
        root.minsize(460, 460)
        self.__addComponets()
        # root.mainloop()

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
        self.canvas.bind('<Button-1>')#, self.clickCanvas)