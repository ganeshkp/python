# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):
    
    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        self.m_menubar1 = wx.MenuBar( 0 )
        self.file = wx.Menu()
        self.m_menu1 = wx.Menu()
        self.file.AppendSubMenu( self.m_menu1, u"New" )
        
        self.m_menu2 = wx.Menu()
        self.file.AppendSubMenu( self.m_menu2, u"Open" )
        
        self.m_menubar1.Append( self.file, u"File" ) 
        
        self.exit = wx.Menu()
        self.m_menubar1.Append( self.exit, u"help" ) 
        
        self.SetMenuBar( self.m_menubar1 )
        
        
        self.Centre( wx.BOTH )
    
    def __del__( self ):
        pass
    
if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame1(parent=None)
    frame.Show()
    app.MainLoop()
