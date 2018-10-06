############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.6.5
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
import logging
import platform
# external packages
import PyQt5.QtWidgets
import PyQt5.QtGui
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
# local imports
import base.styles
import base.tpool
import mw4_global


version = '0.1'
__all__ = [
    'MWidget',
]


class MWidget(PyQt5.QtWidgets.QWidget, base.styles.MWStyles):
    """
    MWidget defines the common parts for all windows used in MountWizzard 4. namely the
    sizes and the styles. styles are defined separately in a css looking stylesheet.
    standard screen size will be 800x600 pixel
    """

    __all__ = ['closeEvent',
               'wIcon',
               'initUI',
               'changeStyleSheet',
               'clearPolar',
               'integrateMatplotlib',
               ]

    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.palette = PyQt5.QtGui.QPalette()
        self.initUI()
        self.screenSizeX = PyQt5.QtWidgets.QDesktopWidget().screenGeometry().width()
        self.screenSizeY = PyQt5.QtWidgets.QDesktopWidget().screenGeometry().height()
        self.showStatus = False

    def closeEvent(self, closeEvent):
        self.showStatus = False
        self.hide()

    @staticmethod
    def wIcon(gui, icon):
        """
        widget icon adds an icon to a gui element like an button.

        :param      gui:        gui element, which will be expanded by an icon
        :param      icon:       icon to be added
        :return:    nothing
        """

        iconset = PyQt5.QtWidgets.qApp.style().standardIcon(icon)
        gui.setIcon(PyQt5.QtGui.QIcon(iconset))
        gui.setProperty('iconset', True)
        gui.style().unpolish(gui)
        gui.style().polish(gui)
        gui.setIconSize(PyQt5.QtCore.QSize(16, 16))

    def initUI(self):
        """
        init_UI makes the basic initialisation of the GUI. is sets the window flags
        and sets the handling of the window. is as well fixes the windows size (unless
        a windows will be scalable later on. in addition the appropriate style sheet
        for mac and non mac will be selected and used.

        :return:    nothing
        """

        self.setWindowFlags(self.windowFlags()
                            )
        self.setMouseTracking(True)
        self.setWindowIcon(PyQt5.QtGui.QIcon(':/mw4.ico'))
        if platform.system() == 'Darwin':
            self.setStyleSheet(self.MAC_STYLE + self.BASIC_STYLE)
        else:
            self.setStyleSheet(self.NON_MAC_STYLE + self.BASIC_STYLE)

    @staticmethod
    def changeStylesheet(ui, item, value):
        """
        changeStylesheet changes the stylesheet of a given uii element and makes it
        visible. therefore the element has to be unpolished and polished again.

        :param      ui:     ui element, where the stylesheet has to be changed
        :param      item:   stylesheet attribute which has to be changes
        :param      value:  new value of the attribute
        :return:    nothing
        """

        ui.style().unpolish(ui)
        ui.setProperty(item, value)
        ui.style().polish(ui)

    @staticmethod
    def clearPolar(widget):
        """
        clearPolar clears and setups the canvas widget for drawing. it sets the labels,
        ticks and some other ui styles.

        :param      widget:    matplotlib canvas widget for drawing
        :return:    fig        figure in widget
        :return:    axes       axes in figure
        """

        fig = widget.figure
        fig.clf()
        axes = fig.add_subplot(1,
                               1,
                               1,
                               polar=True)
        axes.grid(True,
                  color='#404040',
                  )
        axes.set_title('Actual Mount Model',
                       color='white',
                       fontweight='bold',
                       pad=15,
                       )
        fig.subplots_adjust(left=0.07,
                            right=1,
                            bottom=0.03,
                            top=0.97,
                            )
        axes.set_facecolor((32 / 256, 32 / 256, 32 / 256))
        axes.tick_params(axis='x',
                         colors='#2090C0',
                         labelsize=12,
                         )
        axes.tick_params(axis='y',
                         colors='#2090C0',
                         labelsize=12,
                         )
        axes.set_theta_zero_location('N')
        axes.set_theta_direction(-1)
        axes.set_yticks(range(0, 90, 10))
        yLabel = ['', '', '', '', '', '', '', '', '', '']
        axes.set_yticklabels(yLabel,
                             color='#2090C0',
                             fontweight='bold')
        axes.set_rlabel_position(45)
        return fig, axes

    @staticmethod
    def integrateMatplotlib(ui):
        """
        IntMatplotlib provides the wrapper to use matplotlib drawings inside a pyqt5
        application gui. you call it with the parent widget, which is linked to matplotlib
        canvas of the same size. the background is set to transparent, so you could layer
        multiple figures on top.

        :param      ui:             parent ui element, which is the reference for embedding
        :return:    staticCanvas:   matplotlib reference as parent for figures
        """

        # to avoid a white flash before drawing on top.
        ui.setStyleSheet("background:transparent;")
        layout = PyQt5.QtWidgets.QVBoxLayout(ui)
        layout.setContentsMargins(0, 0, 0, 0)
        staticCanvas = FigureCanvas(Figure(dpi=75,
                                           facecolor=(0.1, 0.1, 0.1),
                                           )
                                    )
        FigureCanvasQTAgg.setSizePolicy(staticCanvas,
                                        PyQt5.QtWidgets.QSizePolicy.Expanding,
                                        PyQt5.QtWidgets.QSizePolicy.Expanding
                                        )
        FigureCanvasQTAgg.updateGeometry(staticCanvas)
        layout.addWidget(staticCanvas)
        return staticCanvas

    @staticmethod
    def prepareFileDialog(window):
        """
        prepareFileDialog does some preparations for geometry and general settings

        :param window:  parent class
        :return:        dlg, the dialog widget
        """

        dlg = PyQt5.QtWidgets.QFileDialog()
        dlg.setWindowIcon(PyQt5.QtGui.QIcon(':/mw4.ico'))
        dlg.setStyleSheet('background-color: rgb(32,32,32); color: rgb(192,192,192)')
        dlg.setViewMode(PyQt5.QtWidgets.QFileDialog.List)
        dlg.setFileMode(PyQt5.QtWidgets.QFileDialog.ExistingFile)
        dlg.setModal(True)
        # position the window to parent in the center
        ph = window.geometry().height()
        px = window.geometry().x()
        py = window.geometry().y()
        dw = window.width()
        dh = window.height()
        dlg.setGeometry(px, py + ph - dh, dw, dh)
        return dlg

    @staticmethod
    def openFile(window, title, folder, filterSet):
        dlg = self.propareFileDialog(window)
        dlg.setNameFilter(filterSet)
        ext = ''
        options = PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        value = dlg.getOpenFileName(dlg,
                                    title,
                                    mw4_global.work_dir + folder,
                                    filterSet,
                                    options=options)
        name = value[0]
        if len(name) > 0:
            name, ext = os.path.splitext(name)
        return name, ext

    @staticmethod
    def saveFile(window, title, folder, filterSet):
        dlg = self.propareFileDialog(window)
        dlg.setNameFilter(filterSet)
        ext = ''
        options = PyQt5.QtWidgets.QFileDialog.DontUseNativeDialog
        value = dlg.getSaveFileName(dlg,
                                    title,
                                    mw4_global.work_dir + folder,
                                    filterSet,
                                    options=options)
        name = value[0]
        if len(name) > 0:
            name, ext = os.path.splitext(name)
        return name, ext
