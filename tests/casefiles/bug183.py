#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# generated by wxGlade
#

import wx

# begin wxGlade: dependencies
import gettext
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class Bug183_UI_Frame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Bug183_UI_Frame.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle(_("frame_1"))
        
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        
        self.label_1 = wx.StaticText(self, wx.ID_ANY, _("Just a label"))
        sizer_1.Add(self.label_1, 1, wx.ALL | wx.EXPAND, 5)
        
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        
        self.Layout()
        # end wxGlade

# end of class Bug183_UI_Frame

class Bug173_UI_SomeDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: Bug173_UI_SomeDialog.__init__
        kwds["style"] = kwds.get("style", 0)
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle(_("dialog_1"))
        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self.label_2 = wx.StaticText(self, wx.ID_ANY, _("Just another label"))
        sizer_2.Add(self.label_2, 1, wx.ALL | wx.EXPAND, 5)
        
        self.SetSizer(sizer_2)
        sizer_2.Fit(self)
        
        self.Layout()
        # end wxGlade

# end of class Bug173_UI_SomeDialog

class MyApp(wx.App):
    def OnInit(self):
        self.Frame183 = Bug183_UI_Frame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.Frame183)
        self.Frame183.Show()
        return True

# end of class MyApp

if __name__ == "__main__":
    gettext.install("app") # replace with the appropriate catalog name

    app = MyApp(0)
    app.MainLoop()
