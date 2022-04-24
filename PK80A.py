import win32gui, win32con
import tkinter as tk
from tkinter import ttk
import pyautogui 
import os
from PIL import Image
import pyocr
from time import sleep
import datetime
import pandas as pd
import csv
import socket

host = socket.gethostname()

#インストールしたTesseract-OCRのパスを環境変数「PATH」へ追記する。
#OS自体に設定してあれば以下の2行は不要
path='C:\\Program Files\\Tesseract-OCR'
os.environ['PATH'] = os.environ['PATH'] + path

#pyocrへ利用するOCRエンジンをTesseractに指定する。
tools = pyocr.get_available_tools()
tool = tools[0]

df_settei = pd.read_csv('PK80.csv')
path =  df_settei.iloc[18,1]   #ファイル保存パス

print(df_settei)
print(df_settei.iloc[0,1])



#time初期化
t_delta = datetime.timedelta(hours=9)
JST = datetime.timezone(t_delta, 'JST')

def foreground_on(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        #最前面ON
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return

def foreground_off(hwnd, title):
    name = win32gui.GetWindowText(hwnd)
    if name.find(title) >= 0:
        #最前面OFF
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return


def capture_and_click_OK():

    #時刻を取得
    now = datetime.datetime.now(JST)
    yyyymmdd_hhmmss = now.strftime('%Y%m%d_%H%M%S')

    pos = pyautogui.position()  #マウスの座標を取得

    #全画面保存
    screen_shot = pyautogui.screenshot(region=(0,0, df_settei.iloc[16,1], df_settei.iloc[17,1]))   #右 下、 幅、高さ
    screen_shot.save( path  + yyyymmdd_hhmmss + '_OK_' + host + '.png' )

    # #検査画像保存
    # screen_shot = pyautogui.screenshot(region=(df_settei.iloc[0,1], df_settei.iloc[1,1], df_settei.iloc[2,1], df_settei.iloc[3,1]))   #右 下、 幅、高さ
    # screen_shot.save(yyyymmdd_hhmmss + '_10kensa.png')

    # #正常画像保存
    # screen_shot = pyautogui.screenshot(region=(df_settei.iloc[4,1], df_settei.iloc[5,1], df_settei.iloc[6,1], df_settei.iloc[7,1]))   #右 下、 幅、高さ
    # screen_shot.save(yyyymmdd_hhmmss + '_20seijo.png')

    # #不良メッセージ保存
    # screen_shot = pyautogui.screenshot(region=(df_settei.iloc[8,1], df_settei.iloc[9,1], df_settei.iloc[10,1], df_settei.iloc[11,1]))   #右 下、 幅、高さ
    # screen_shot.save(yyyymmdd_hhmmss + '_30comnt.png')

    # #OCR対象の画像ファイルを読み込む
    # img = Image.open(yyyymmdd_hhmmss + '_30comnt.png')

    # #画像から文字を読み込む
    # builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    # text = tool.image_to_string(img, lang="jpn", builder=builder)

    # #CSV出力 
    # #print(text)
    # f = open(yyyymmdd_hhmmss + '_OK.csv', 'w')
    # data = [yyyymmdd_hhmmss, 'OK' , text]
    # writer = csv.writer(f)
    # writer.writerow(data)
    # f.close()

    #OKボタンクリック
    pyautogui.click(df_settei.iloc[0,1], df_settei.iloc[1,1])    #画面をactiveにするため一度クリックする。 検査画像の座標
    pyautogui.moveTo(df_settei.iloc[12,1], df_settei.iloc[13,1])  #マウス移動 OKボタン
    pyautogui.click(df_settei.iloc[12,1], df_settei.iloc[13,1])   #クリック  OKボタン
    pyautogui.moveTo(pos.x, pos.y) #マウス移動 元の位置へ


def capture_and_click_NG():

    #時刻を取得
    now = datetime.datetime.now(JST)
    yyyymmdd_hhmmss = now.strftime('%Y%m%d_%H%M%S')

    pos = pyautogui.position()  #マウスの座標を取得

    #全画面保存
    screen_shot = pyautogui.screenshot(region=(0,0, df_settei.iloc[16,1], df_settei.iloc[17,1]))   #右 下、 幅、高さ
    screen_shot.save( path  + yyyymmdd_hhmmss + '_NG_' + host + '.png' )


    # #検査画像保存
    # screen_shot = pyautogui.screenshot(region=(df_settei.iloc[0,1], df_settei.iloc[1,1], df_settei.iloc[2,1], df_settei.iloc[3,1]))   #右 下、 幅、高さ
    # screen_shot.save(yyyymmdd_hhmmss + '_10kensa.png')

    # #正常画像保存
    # screen_shot = pyautogui.screenshot(region=(df_settei.iloc[4,1], df_settei.iloc[5,1], df_settei.iloc[6,1], df_settei.iloc[7,1]))   #右 下、 幅、高さ
    # screen_shot.save(yyyymmdd_hhmmss + '_20seijo.png')

    # #不良メッセージ保存
    # screen_shot = pyautogui.screenshot(region=(df_settei.iloc[8,1], df_settei.iloc[9,1], df_settei.iloc[10,1], df_settei.iloc[11,1]))   #右 下、 幅、高さ
    # screen_shot.save(yyyymmdd_hhmmss + '_30comnt.png')

    # #OCR対象の画像ファイルを読み込む
    # img = Image.open(yyyymmdd_hhmmss + '_30comnt.png')

    # #画像から文字を読み込む
    # builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    # text = tool.image_to_string(img, lang="jpn", builder=builder)

    # #CSV出力 
    # #print(text)
    # f = open(yyyymmdd_hhmmss + '_NG.csv', 'w')
    # data = [yyyymmdd_hhmmss, 'NG' , text]
    # writer = csv.writer(f)
    # writer.writerow(data)
    # f.close()

    #NGボタンクリック
    pyautogui.click(df_settei.iloc[0,1], df_settei.iloc[1,1])    #画面をactiveにするため一度クリックする。 検査画像の座標
    pyautogui.moveTo(df_settei.iloc[14,1], df_settei.iloc[15,1])  #マウス移動 NGボタン
    pyautogui.click(df_settei.iloc[14,1], df_settei.iloc[15,1])   #クリック  NGボタン
    pyautogui.moveTo(pos.x, pos.y) #マウス移動 元の位置へ




GAMEN_NAME ='PK80A'
mainWnd = tk.Tk()
mainWnd.title(GAMEN_NAME)
mainWnd.geometry("800x100")

def Button_1():
    #value = EditBox.get()
    value = GAMEN_NAME
    win32gui.EnumWindows(foreground_on, value)

def Button_2():
    #value = EditBox.get()
    value = GAMEN_NAME
    win32gui.EnumWindows(foreground_off, value)

# def Button_OK():
#     #value = EditBox.get()
#     # value = GAMEN_NAME
#     # win32gui.EnumWindows(foreground_off, value)
#     capture_and_click('OK')

# def Button_NG():
#     #value = EditBox.get()
#     # value = GAMEN_NAME
#     # win32gui.EnumWindows(foreground_off, value)
#     capture_and_click('NG')

#エントリー
# EditBox = ttk.Entry()
# EditBox.insert(tk.END,GAMEN_NAME)
# EditBox.pack(expand = True, fill = tk.BOTH, padx = 5, pady = 5)


#ボタン1
Button1 = ttk.Button(text='最前面ON', command=Button_1) 
#Button1.pack(expand = True, fill = tk.BOTH, padx = 5)
Button1.place(x=20,y=0,width=200,height=100)  #x:左右  y:上下

#ボタン2
Button2 = ttk.Button(text='OK', command=capture_and_click_OK) 
#Button2.pack(expand = True, fill = tk.BOTH, padx = 5, pady = 5)
Button2.place(x=250,y=00,width=200,height=100)

#ボタン2
Button2 = ttk.Button(text='NG', command=capture_and_click_NG) 
#Button2.pack(expand = True, fill = tk.BOTH, padx = 5, pady = 5)
Button2.place(x=500,y=00,width=200,height=100)

mainWnd.mainloop()