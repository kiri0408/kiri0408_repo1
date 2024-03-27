import tkinter

# pip install cx-Freeze
# cxfreeze -c a11.py --target-dir a11

def test():
    for i in range(10):
        print(i)


# 画面作成
window = tkinter.Tk()
window.geometry("400x300")
window.title("ボタンを表示する")
# ボタン作成
btn = tkinter.Button(window, text="ボタン" ,command=lambda:test())
# ボタン表示
btn.place(x=125, y=230, width=150, height=40)
# 画面表示（常駐）
window.mainloop()

