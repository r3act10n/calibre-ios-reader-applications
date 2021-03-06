#!/usr/bin/env python
#!/usr/bin/env python
# coding: utf-8

from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2010, Gregory Riker'
__docformat__ = 'restructuredtext en'

import os, sys

from calibre.devices.usbms.driver import debug_print

from calibre_plugins.ios_reader_apps.config import widget_path

from PyQt4.Qt import QWidget

# Import Ui_Form from form generated dynamically during initialization
if True:
    sys.path.insert(0, widget_path)
    from <ios_reader_app>_ui import Ui_Form
    sys.path.remove(widget_path)


class PluginWidget(QWidget, Ui_Form):

    LOCATION_TEMPLATE = "{cls}:{func}({arg1}) {arg2}"

    TITLE = '<iOS reader app> Options'

    def __init__(self, parent):
        QWidget.__init__(self, parent=None)
        self.setupUi(self)
        self.parent = parent
        self.verbose = parent.verbose
        self._log_location()

    def initialize(self, name):
        '''
        Retrieve plugin-specific settings from general prefs store
        '''
        self.name = name
        self._log_location(name)
        for pref in self.parent.prefs:
            if pref.startswith(self.name) and hasattr(self, pref):
                opt_value = self.parent.prefs[pref]
                self._log("setting pref '%s' to %s" % (pref, repr(opt_value)))
                if type(getattr(self, pref)) is QLineEdit:
                    getattr(self, pref).setText(opt_value if opt_value else '')
                elif type(getattr(self, pref)) is QCheckBox:
                    getattr(self, pref).setChecked(eval(str(opt_value)))

    def options(self):
        '''
        Return a dict of the current field values
        '''
        self._log_location()
        return {}

    def _log(self, msg=None):
        '''
        Print msg to console
        '''
        if not self.verbose:
            return

        if msg:
            debug_print(" %s" % msg)
        else:
            debug_print()

    def _log_location(self, *args):
        '''
        Print location, args to console
        '''
        if not self.verbose:
            return

        arg1 = arg2 = ''

        if len(args) > 0:
            arg1 = args[0]
        if len(args) > 1:
            arg2 = args[1]

        debug_print(self.LOCATION_TEMPLATE.format(
            #cls=self.__class__.__name__,
            cls = self.TITLE,
            func=sys._getframe(1).f_code.co_name,
            arg1=arg1, arg2=arg2))

