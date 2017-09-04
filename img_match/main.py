#! env python
# -*- coding: utf-8 -*-

import wx
import sys,os

if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, wx.ID_ANY, "Main")

# ボタンの作成
panel = wx.Panel(frame, wx.ID_ANY)
panel.SetBackgroundColour("#AFAFAF")
button_1 = wx.Button(panel, wx.ID_ANY, u"ボタン１")
button_2 = wx.Button(panel, wx.ID_ANY, u"ボタン２")
button_3 = wx.Button(panel, wx.ID_ANY, u"ボタン３")
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(button_1, proportion=1)
layout.Add(button_2, proportion=1)
layout.Add(button_3, proportion=1)
panel.SetSizer(layout)

# ファイル選択ダイアログを作成
dialog = wx.FileDialog(None, u'ファイルを選択してください')

# ファイル選択ダイアログを表示
dialog.ShowModal()
frame.Show()
app.MainLoop()
