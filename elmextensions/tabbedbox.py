'''A simple tabbed Box implementation.'''
from efl.elementary.box import Box
from efl.elementary.button import Button
from efl.elementary.icon import Icon
from efl.elementary.naviframe import Naviframe
from efl.elementary.separator import Separator
from efl.elementary.scroller import Scroller
# pylint: disable=no-name-in-module
from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL

EXPAND_BOTH = EVAS_HINT_EXPAND, EVAS_HINT_EXPAND
EXPAND_HORIZ = EVAS_HINT_EXPAND, 0.0
FILL_BOTH = EVAS_HINT_FILL, EVAS_HINT_FILL
FILL_HORIZ = EVAS_HINT_FILL, 0.5
EXPAND_NONE = 0.0, 0.0
ALIGN_CENTER = 0.5, 0.5
ALIGN_RIGHT = 1.0, 0.5
ALIGN_LEFT = 0.0, 0.5


class TabbedBox(Box):
    '''A TabbedBox class.'''

    def __init__(self, parent_widget, *args, **kwargs):
        Box.__init__(self, parent_widget, *args, **kwargs)

        self.tabs = []
        self.current = None

        self.scr = Scroller(self,
                            size_hint_weight=EXPAND_HORIZ,
                            size_hint_align=FILL_BOTH)
        self.scr.content_min_limit(False, True)

        self.btn_bx = Box(self.scr,
                          size_hint_weight=EXPAND_HORIZ,
                          align=ALIGN_LEFT)
        self.btn_bx.horizontal = True
        self.btn_bx.show()

        self.scr.content = self.btn_bx
        self.scr.show()

        self.nav_fr = Naviframe(self,
                                size_hint_weight=EXPAND_BOTH,
                                size_hint_align=FILL_BOTH)
        self.nav_fr.show()

        self.pack_end(self.scr)
        self.pack_end(self.nav_fr)

    def add(self, widget, name, can_close=True, disabled=False):
        '''Add a tab to the tabbed box'''
        self.tabs.append(widget)

        btn = Button(self.btn_bx, style="anchor", size_hint_align=ALIGN_LEFT)
        btn.text = name
        btn.data["widget"] = widget
        btn.disabled = disabled
        btn.callback_clicked_add(self.showTab, widget)
        btn.show()

        icn = Icon(self.btn_bx)
        icn.standard_set("gtk-close")
        icn.show()

        cls = Button(self.btn_bx,
                     content=icn,
                     style="anchor",
                     size_hint_align=ALIGN_LEFT)
        cls.data["widget"] = widget
        cls.callback_clicked_add(self.closeTab)
        cls.disabled = disabled
        if can_close:
            cls.show()

        sep = Separator(self.btn_bx, size_hint_align=ALIGN_LEFT)
        sep.show()

        self.btn_bx.pack_end(btn)
        self.btn_bx.pack_end(cls)
        self.btn_bx.pack_end(sep)

        # Arguments go: btn, cls, sep
        widget.data["close"] = cls
        widget.data["button"] = btn
        widget.data["sep"] = sep

        self.showTab(widget=widget)

    def disable(self, tab_index):
        '''Disable a tab'''
        btn, cls = self.tabs[tab_index].data["button"], self.tabs[
            tab_index].data["close"]
        btn.disabled = True
        cls.disabled = True

    def enable(self, tab_index):
        '''Enable a tab'''
        btn, cls = self.tabs[tab_index].data["button"], self.tabs[
            tab_index].data["close"]
        btn.disabled = False
        cls.disabled = False

    def show(self, btn=None, widget=None):
        '''Show tab'''
        # pylint: disable=unidiomatic-typecheck
        #   This is as clear as any alternative to me
        if type(btn) is int:
            widget = self.tabs[btn]
        if widget != self.current:
            if self.current:
                self.current.data["button"].style = "anchor"
            self.nf.item_simple_push(widget)
            self.current = widget
            self.current.data["button"].style = "widget"

            if self.tabChangedCallback:
                self.tabChangedCallback(self, widget)

    def close(self, btn):
        '''Close tab'''
        self.delete(btn.data["widget"])

    def delete(self, widget):
        '''Delete tab'''
        # pylint: disable=unidiomatic-typecheck
        #   This is as clear as any alternative to me
        if type(widget) is int:
            widget = self.tabs[widget]

        del self.tabs[self.tabs.index(widget)]

        self.btn_bx.unpack(widget.data["close"])
        self.btn_bx.unpack(widget.data["button"])
        self.btn_bx.unpack(widget.data["sep"])

        widget.data["close"].delete()
        widget.data["button"].delete()
        widget.data["sep"].delete()
        widget.delete()

        if self.current == widget and self.tabs:
            self.showTab(widget=self.tabs[0])

        # if not self.tabs and self.emptyCallback:
        #    self.emptyCallback(self)
