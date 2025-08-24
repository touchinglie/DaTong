import tkinter as tk
import tkinter.ttk as ttk

import utils.dataloader as dr


def CloseWindows() -> None:
    global mainWindows
    mainWindows.destroy()


def ImportWidget():
    Url = tk.StringVar()

    inputWindow = tk.Toplevel()
    inputUrl = tk.Entry(inputWindow, textvariable=Url)
    inputUrl.place(x=30, y=30)

    CheckInputBut = tk.Button(inputWindow, text="确定", command=None)


mainWindows = tk.Tk()

mainWindows.title("大同")
mainWindows.geometry("320x200")

MainMenu = tk.Menu(mainWindows)

FileMenu = tk.Menu(MainMenu)
OutPutMenu = tk.Menu(MainMenu)
MainMenu.add_cascade(label="文件", menu=FileMenu)
MainMenu.add_cascade(label="导出格式", menu=OutPutMenu)

FileMenu.add_command(label="关闭", command=CloseWindows)
FileMenu.add_command(label="加载数据集", command=ImportWidget)

mainWindows.config(menu=MainMenu)


mainWindows.mainloop()
