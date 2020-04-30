import efl.elementary as elm

from efl.elementary.window import StandardWindow
from efl.elementary.label import Label
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

from elmextensions import TabbedBox

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL

class MainWindow(object):
    def __init__( self ):
        win = StandardWindow("Testing", "Elementary Tabbed Widget")
        win.callback_delete_request_add(lambda o: elm.exit())

        tabbs = TabbedBox(win, size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        tabbs.closeCallback = self.closeChecks
        
        for i in range(10):
            lbl = Label(win)
            lbl.text = "Tab %s"%i
            lbl.show()
            tabbs.add(lbl, "Tab %s"%i)
        
        tabbs.disable(0)
        tabbs.disable(3)
        
        tabbs.show()
        
        win.resize_object_add(tabbs)

        win.resize(600, 400)
        win.show()
    
    def closeChecks(self, tabbs, widget):
        print(widget.text)
        if widget.text != "Tab 1":
            tabbs.deleteTab(widget)

if __name__ == "__main__":
    elm.init()
    GUI = MainWindow()
    elm.run()
    elm.shutdown()
