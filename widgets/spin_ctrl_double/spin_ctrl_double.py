"""\
wxSpinCtrlDouble objects

@copyright: 2002-2007 Alberto Griggio
@copyright: 2014-2016 Carsten Grohmann
@copyright: 2016-2018 Dietmar Schwertberger
@license: MIT (see LICENSE.txt) - THIS PROGRAM COMES WITH NO WARRANTY
"""

import wx
from edit_windows import ManagedBase, EditStylesMixin
from tree import Node
import common, config
import new_properties as np


class EditSpinCtrlDouble(ManagedBase, EditStylesMixin):
    "Class to handle wxSpinCtrlDouble objects"
    # XXX unify with EditSpinButton?
    _PROPERTIES = ["Widget", "range", "value", "increment", "style"]
    PROPERTIES = ManagedBase.PROPERTIES + _PROPERTIES + ManagedBase.EXTRA_PROPERTIES

    def __init__(self, name, parent, pos):
        ManagedBase.__init__(self, name, 'wxSpinCtrlDouble', parent, pos)
        EditStylesMixin.__init__(self)

        # initialise instance properties
        self.range = np.FloatRangePropertyA( "0.0, 100.0" )
        self.value = np.SpinDoublePropertyA(0, val_range=(0.0,100.0), immediate=True, default_value="")
        self.increment = np.SpinDoublePropertyD(1.0, val_range=(0.0,100.0), immediate=True, default_value=1.0)

    def create_widget(self):
        mi,ma = self.properties["range"].get_tuple()
        kwargs = {}
        if self.properties["value"].is_active():
            kwargs["initial"] = self.value
        if self.properties["increment"].is_active():
            kwargs["inc"] = self.value
        window = self.parent_window
        self.widget = wx.SpinCtrlDouble(window.widget, self.id, min=mi, max=ma, **kwargs)

    def finish_widget_creation(self, sel_marker_parent=None, re_add=True):
        ManagedBase.finish_widget_creation(self, sel_marker_parent, re_add)
        self.widget.Bind(wx.EVT_CHILD_FOCUS, self.on_set_focus)
        self.widget.Bind(wx.EVT_SPIN, self.on_set_focus)

    def properties_changed(self, modified):  # from EditSlider
        if not modified or "range" in modified and self.widget:
            mi,ma = self.properties["range"].get_tuple()
            self.widget.SetRange(mi, ma)
            self.properties["value"].set_range(mi,ma)
            self.properties["increment"].set_range(mi,ma)

        if not modified or "increment" in modified and self.widget:
            self.widget.SetIncrement(self.increment)

        if not modified or "value" in modified or "range" in modified:
            # check that value is inside range
            value_p = self.properties["value"]
            if value_p.is_active():
                mi,ma = self.properties["range"].get_tuple()
                value = value_p.get()
                if value<mi:
                    value_p.set(mi)
                    value = mi
                elif value>ma:
                    value_p.set(ma)
                    value = ma
                if self.widget:
                    self.widget.SetValue(value)

        EditStylesMixin.properties_changed(self, modified)
        ManagedBase.properties_changed(self, modified)


def builder(parent, pos, number=[1]):
    "factory function for EditSpinCtrl objects"
    name = 'spin_ctrl_double_%d' % number[0]
    toplevel_parent = parent.toplevel_parent
    while name in toplevel_parent.names:
        number[0] += 1
        name = 'spin_ctrl_double_%d' % number[0]
    with parent.frozen():
        spin = EditSpinCtrlDouble(name, parent, pos)
        spin.properties["style"].set_to_default()
        spin.check_defaults()
        node = Node(spin)
        spin.node = node
        if parent.widget: spin.create()
    common.app_tree.insert(node, parent.node, pos-1)


def xml_builder(attrs, parent, sizeritem, pos=None):
    "factory function to build EditSpinCtrlDouble objects from a XML file"
    from xml_parse import XmlParsingError
    try:
        name = attrs['name']
    except KeyError:
        raise XmlParsingError(_("'name' attribute missing"))
    if sizeritem is None:
        raise XmlParsingError(_("sizer or sizeritem object cannot be None"))
    spin = EditSpinCtrlDouble( name, parent, pos )
    spin.properties["value"].set_active(False)
    #sizer.set_item( spin.pos, proportion=sizeritem.proportion, flag=sizeritem.flag, border=sizeritem.border )
    node = Node(spin)
    spin.node = node
    if pos is None:
        common.app_tree.add(node, parent.node)
    else:
        common.app_tree.insert(node, parent.node, pos-1)
    return spin


#def builder(parent, pos, number=[1]):
    #"factory function for EditSpinCtrl objects"
    #name = 'spin_ctrl_double_%d' % number[0]
    #while common.app_tree.has_name(name):
        #number[0] += 1
        #name = 'spin_ctrl_double_%d' % number[0]
    #with parent.frozen():
        #spin = EditSpinCtrlDouble(name, parent, pos)
        #spin.properties["style"].set_to_default()
        #spin.check_defaults()
        #if parent.widget: spin.create()
    #common.app_tree.build(spin)


#def xml_builder(attrs, parent, sizeritem, pos=None):
    #"factory function to build EditSpinCtrlDouble objects from a XML file"
    #from xml_parse import XmlParsingError
    #try:
        #name = attrs['name']
    #except KeyError:
        #raise XmlParsingError(_("'name' attribute missing"))
    #if sizeritem is None:
        #raise XmlParsingError(_("sizer or sizeritem object cannot be None"))
    #spin = EditSpinCtrlDouble( name, parent, pos )
    #spin.properties["value"].set_active(False)
    ##sizer.set_item( spin.pos, proportion=sizeritem.proportion, flag=sizeritem.flag, border=sizeritem.border )
    #common.app_tree.build(spin)
    #return spin

def initialize():
    "initialization function for the module: returns a wxBitmapButton to be added to the main palette"
    if not hasattr(wx, "SpinCtrlDouble"): return None
    common.widgets['EditSpinCtrlDouble'] = builder
    common.widgets_from_xml['EditSpinCtrlDouble'] = xml_builder

    return common.make_object_button('EditSpinCtrlDouble', 'spin_ctrl_double.xpm')
