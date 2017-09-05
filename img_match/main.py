#! env python
# -*- coding: utf-8 -*-

import wx
import sys,os
import cv2

# 変数の宣言
filepath = ""
folderpath = ""
text1 = ""
button_1 = ""

class MainFrame(wx.Frame):

    # イベント
    def click_button_1(self, event):
        global filepath
        global button_1
        # ファイル選択ダイアログを作成
        dialog = wx.FileDialog(None, u'比較ファイルを選択してください')
        # ファイル選択ダイアログを表示
        dialog.ShowModal()
        # 選択したファイルパスを取得する
        filepath = dialog.GetPath()
        self.SetStatusText(os.path.basename(filepath))
        # ボタンに画像を入れる
        btnBitmap = wx.Bitmap(filepath)
        button_1 = wx.BitmapButton(self, -1, btnBitmap)

    def click_button_2(self, event):
        global folderpath
        # フォルダ選択ダイアログを作成
        dialog = wx.DirDialog(None, u'画像フォルダを選択してください')
        # フォルダ選択ダイアログを表示
        dialog.ShowModal()
        # 選択したフォルダパスを取得する
        folderpath = dialog.GetPath()
        self.SetStatusText(folderpath)

    def click_button_3(self, event):
        global filepath
        global folderpath
        global text1
        TARGET_FILE = os.path.basename(filepath)
        IMG_DIR = folderpath + "/"
        IMG_SIZE = (200, 200)

        target_img_path = IMG_DIR + TARGET_FILE
        target_img = cv2.imread(target_img_path, cv2.IMREAD_GRAYSCALE)
        target_img = cv2.resize(target_img, IMG_SIZE)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        detector = cv2.ORB_create()
        # detector = cv2.AKAZE_create()
        (target_kp, target_des) = detector.detectAndCompute(target_img, None)

        print('TARGET_FILE: %s' % (TARGET_FILE))

        files = os.listdir(IMG_DIR)
        for file in files:
            if file == '.DS_Store' or file == TARGET_FILE:
                continue

            comparing_img_path = IMG_DIR + file
            try:
                comparing_img = cv2.imread(comparing_img_path, cv2.IMREAD_GRAYSCALE)
                comparing_img = cv2.resize(comparing_img, IMG_SIZE)
                (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
                matches = bf.match(target_des, comparing_des)
                dist = [m.distance for m in matches]
                ret = sum(dist) / len(dist)
            except cv2.error:
                ret = 100000

            print(file, ret)
            text1.AppendText(file + " : " + str(ret) + "\n")

    def __init__(self):
         wx.Frame.__init__(self, None, wx.ID_ANY, "Main")
         self.InitializeComponents()

    def InitializeComponents(self):
        global text1
        global button_1
        self.CreateStatusBar()
        # ボタンの作成
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour("#AFAFAF")
        button_1 = wx.Button(panel, wx.ID_ANY, u"比較ファイル")
        button_2 = wx.Button(panel, wx.ID_ANY, u"画像フォルダ")
        button_3 = wx.Button(panel, wx.ID_ANY, u"実行")
        # panel2 = wx.Panel(frame, wx.ID_ANY)
        # panel2.SetBackgroundColour("#000000")
        text1 = wx.TextCtrl(panel, wx.ID_ANY, style=wx.TE_MULTILINE)

        # イベントの設定
        button_1.Bind(wx.EVT_BUTTON, self.click_button_1)
        button_2.Bind(wx.EVT_BUTTON, self.click_button_2)
        button_3.Bind(wx.EVT_BUTTON, self.click_button_3)

        # ボタンレイアウト
        layout = wx.GridBagSizer()
        layout.Add(button_1, (0,0), (1,1), flag=wx.EXPAND)
        layout.Add(button_2, (0,1), (1,1), flag=wx.EXPAND)
        layout.Add(button_3, (0,2), (1,1), flag=wx.EXPAND)
        layout.Add(text1, (1,0), (3,3), flag=wx.EXPAND)
        layout.AddGrowableRow(0)
        layout.AddGrowableRow(1)
        layout.AddGrowableRow(2)
        layout.AddGrowableRow(3)
        layout.AddGrowableCol(0)
        layout.AddGrowableCol(1)
        layout.AddGrowableCol(2)
        panel.SetSizer(layout)

if __name__ == '__main__':
    app = wx.App()
    MainFrame().Show(True)
    app.MainLoop()
