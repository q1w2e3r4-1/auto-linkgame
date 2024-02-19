import tkinter as tk
from PIL import ImageTk, Image
import cv2
import numpy as np
import win32api
import win32gui
import win32con
from PIL import ImageGrab
import time
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 窗体标题  用于定位游戏窗体
import main
from main import getAllSquare, getAllSquareTypes, getAllSquareRecord, canConnect

DEBUG = False
WINDOW_TITLE = "LetsView[屏幕镜像]"
# 时间间隔随机生成 [MIN,MAX]
TIME_INTERVAL_MAX = 0.6
TIME_INTERVAL_MIN = 1
# 游戏区域距离顶点的x偏移
MARGIN_LEFT = 195
# 游戏区域距离顶点的y偏移
MARGIN_HEIGHT = 120
# 横向的方块数量
H_NUM = 10
# 纵向的方块数量
V_NUM = 10
# 方块宽度
POINT_WIDTH = 40
# 方块高度
POINT_HEIGHT = 40
# 空图像编号
EMPTY_ID = 0
# 切片处理时候的左上、右下坐标：
SUB_LT_X = 8
SUB_LT_Y = 8
SUB_RB_X = 32
SUB_RB_Y = 32
# 游戏的最多消除次数
MAX_ROUND = 10000
WINDOW_X = 1000
WINDOW_Y = 100


def debug_init():
    global WINDOW_TITLE, TIME_INTERVAL_MAX, TIME_INTERVAL_MIN, MARGIN_LEFT, MARGIN_HEIGHT, H_NUM, V_NUM, \
        POINT_HEIGHT, POINT_WIDTH, EMPTY_ID, SUB_LT_Y, SUB_RB_Y, SUB_LT_X, SUB_RB_X, MAX_ROUND, WINDOW_X, WINDOW_Y
    WINDOW_TITLE = "连连看"
    # 时间间隔随机生成 [MIN,MAX]
    TIME_INTERVAL_MAX = 0.06
    TIME_INTERVAL_MIN = 0.1
    # 游戏区域距离顶点的x偏移
    MARGIN_LEFT = 297
    # 游戏区域距离顶点的y偏移
    MARGIN_HEIGHT = 145
    # 横向的方块数量
    H_NUM = 10
    # 纵向的方块数量
    V_NUM = 10
    # 方块宽度
    POINT_WIDTH = 50
    # 方块高度
    POINT_HEIGHT = 50
    # 空图像编号
    EMPTY_ID = 0
    # 切片处理时候的左上、右下坐标：
    SUB_LT_X = 8
    SUB_LT_Y = 8
    SUB_RB_X = 42
    SUB_RB_Y = 42
    # 游戏的最多消除次数
    MAX_ROUND = 200
    WINDOW_X = 418
    WINDOW_Y = 182
    main.debug_init()


class MainWindow:
    __Title = "Hinter"
    __windowWidth = 500  # 窗口宽度
    __windowHeigth = 750  # 窗口高度
    POINT_WIDTH = 40
    POINT_HEIGHT = 40
    X_OFFSET = 40
    Y_OFFSET = 80
    PADDING = 3
    colors = ['red', 'yellow', 'green']

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
        self.canvas = tk.Canvas(root, bg='white', width=450, height=700)
        # 插入文字
        # self.text = self.canvas.create_text(100, 320, anchor='nw', text='哆啦A梦连连看', fill="white", fon=('华文彩云', 30))
        self.canvas.pack(side=tk.TOP, pady=5)
        self.canvas.bind('<Button-1>', self.func)  # , self.clickCanvas)

    def pos(self, i, j):
        x = self.X_OFFSET + j * self.POINT_WIDTH + self.PADDING
        y = self.Y_OFFSET + i * self.POINT_HEIGHT + self.PADDING
        return x, y

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
                idx = j * 10 + i
                image = Image.fromarray(np.array(square_list[idx]))
                self.photos[i][j] = ImageTk.PhotoImage(image)

                self.canvas.create_image(self.pos(i, j), image=self.photos[i][j], anchor='nw', tags='im%d%d' % (i, j))

    def hint(self, i, j, m, n, prior):
        p1 = self.pos(i, j) + (15, 15)
        p2 = self.pos(m, n) + (15, 15)
        self.canvas.create_oval(p1[0], p1[1], p1[0] + 25, p1[1] + 25, fill=self.colors[prior])
        self.canvas.create_oval(p2[0], p2[1], p2[0] + 25, p2[1] + 25, fill=self.colors[prior])

    def func(self, event):
        # ii. 获取屏幕截图
        screen_image = main.getScreenImage()
        # screen_image = cv2.imread("screen.png")  # TODO
        # iii. 对截图切片，形成一张二维地图
        all_square_list = getAllSquare(screen_image, game_pos)
        # iii-2 创建窗体并绘制图像
        hinter.draw_square(all_square_list, H_NUM, V_NUM)
        print(POINT_WIDTH)
        # iv. 获取所有类型的图形，并编号
        types = getAllSquareTypes(all_square_list)
        # print(type(types))
        # v. 讲获取的图片地图转换成数字矩阵
        result = np.transpose(getAllSquareRecord(all_square_list, types))
        # vi. 执行消除 , 并输出消除数量
        # print('The total elimination amount is ' + str(autoRemove(result, game_pos)))
        autoHint(result)


def hint_one(result, prior):
    # 遍历地图
    # time.sleep(3)
    for i in range(0, len(result)):
        for j in range(0, len(result[0])):
            # 当前位置非空
            if result[i][j] != EMPTY_ID:
                # 再次遍历地图 寻找另一个满足条件的图片
                for m in range(0, len(result)):
                    for n in range(0, len(result[0])):
                        if result[m][n] != EMPTY_ID:
                            # 若可以执行消除
                            if canConnect(i, j, m, n, result):
                                # 消除的两个位置设置为空
                                result[i][j] = EMPTY_ID
                                result[m][n] = EMPTY_ID
                                print('We can remove ：' + str(i) + ',' + str(j) + ' and ' + str(m) + ',' + str(
                                    n) + ", prior =", prior)
                                hinter.hint(i - 1, j - 1, m - 1, n - 1, prior)
                                # # 计算当前两个位置的图片在游戏中应该存在的位置
                                # x1 = game_x + (j - 1) * POINT_WIDTH
                                # y1 = game_y + (i - 1) * POINT_HEIGHT
                                # x2 = game_x + (n - 1) * POINT_WIDTH
                                # y2 = game_y + (m - 1) * POINT_HEIGHT
                                # print("pos: " + str((x1, y1)) + " " + str((x2, y2)))
                                # # 模拟鼠标点击第一个图片所在的位置
                                # win32api.SetCursorPos((x1 + POINT_WIDTH // 2, y1 + POINT_HEIGHT // 2))
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x1 + POINT_WIDTH // 2,
                                #                      y1 + POINT_HEIGHT // 2, 0, 0)
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x1 + POINT_WIDTH // 2,
                                #                      y1 + POINT_HEIGHT // 2, 0, 0)
                                #
                                # # 等待随机时间 ，防止检测
                                # time.sleep(random.uniform(TIME_INTERVAL_MIN, TIME_INTERVAL_MAX))
                                #
                                # # 模拟鼠标点击第二个图片所在的位置
                                # win32api.SetCursorPos((x2 + POINT_WIDTH // 2, y2 + POINT_HEIGHT // 2))
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x2 + POINT_WIDTH // 2,
                                #                      y2 + POINT_HEIGHT // 2, 0, 0)
                                # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x2 + POINT_WIDTH // 2,
                                #                      y2 + POINT_HEIGHT // 2, 0, 0)
                                # time.sleep(random.uniform(TIME_INTERVAL_MIN, TIME_INTERVAL_MAX))
                                # 执行消除后返回True
                                return True
    return False


def autoHint(squares):
    cnt = 0
    # 重复一次消除直到到达最多消除次数
    while cnt < 3:
        print('haha')
        if not hint_one(squares, cnt):
            # 当不再有可消除的方块时结束 ， 返回消除数量
            return cnt
        # time.sleep(1.0)
        cnt += 1


if __name__ == '__main__':
    root = tk.Tk()
    if DEBUG:
        debug_init()
    random.seed()
    hinter = MainWindow()

    # i. 定位游戏窗体
    game_pos = main.getGameWindow()
    hinter.game_pos = game_pos
    # time.sleep(1)
    # # ii. 获取屏幕截图
    screen_image = main.getScreenImage()
    # # screen_image = cv2.imread("screen.png")  # TODO
    # # iii. 对截图切片，形成一张二维地图
    all_square_list = getAllSquare(screen_image, game_pos)
    # # iii-2 创建窗体并绘制图像
    # hinter.draw_square(all_square_list, H_NUM, V_NUM)
    # print(POINT_WIDTH)
    # # iv. 获取所有类型的图形，并编号
    # types = getAllSquareTypes(all_square_list)
    # # print(type(types))
    # # v. 讲获取的图片地图转换成数字矩阵
    # result = np.transpose(getAllSquareRecord(all_square_list, types))
    # # vi. 执行消除 , 并输出消除数量
    # # print('The total elimination amount is ' + str(autoRemove(result, game_pos)))
    # autoHint(result)
    root.mainloop()
