# -*- coding: utf-8; Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-

from ubiquity import misc, plugin, validation
import os
import inspect
import gettext


NAME = 'lliurexDesktopLayout'
AFTER = 'console_setup'
BEFORE = 'usersetup'
WEIGHT = 12

gettext.textdomain('ubilliurexdesktoplayout')
_ = gettext.gettext

class PageKde(plugin.PluginUI):
    plugin_title = 'lliurex/securityUpgrades'

    def __init__(self, controller, *args, **kwargs):
        os.system('mkdir -p /run/user/999/ubiquity')
        with open('/run/user/999/ubiquity/ubilliurexlayout','w') as fd:
            fd.write('default')
        from PyQt5.QtGui import QPixmap, QIcon, QFont
        from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QScrollArea, QGridLayout, QHBoxLayout, QLabel, QSizePolicy, QRadioButton
        from PyQt5.QtCore import Qt
        self.controller = controller
        self.translations = {"defaultlayout":"Default layout", "defaultlayoutdescription": "LliureX show two bars", "classiclayout" : "Classic layout","classiclayoutdescription" : "LliureX show one bar"}
        self.main_widget = QFrame()
        self.main_widget.setLayout(QVBoxLayout())
        qsa = QScrollArea()
        widget = QWidget()
        widget.setLayout(QVBoxLayout())
        widget.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        qsa.setWidget(widget)
        qsa.setWidgetResizable(True)

        self.main_widget.layout().addWidget(qsa)

        widget.layout().addLayout(self.createDefaultLayout(False),False)
        widget.layout().addLayout(self.createClassicLayout(True),True)

        self.page = widget
        self.plugin_widgets = self.page

    def createDefaultLayout(self,last):
        from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
        from PyQt5.QtCore import Qt
        gLayout = QGridLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        verticalLayout = QVBoxLayout()
        verticalLayout.setObjectName("verticalLayout")
        horizontalLayout.addLayout(verticalLayout)

        image_package = self.createImage('/usr/share/plasma/look-and-feel/lliurex-desktop/contents/previews/preview.png')
        self.default_name = self.createName(_(self.translations['defaultlayout']))
        self.default_description = self.createDescription(_(self.translations['defaultlayoutdescription']))
        default_check = self.createRadio('default',True)

        verticalLayout.addWidget(self.default_name)
        verticalLayout.addWidget(self.default_description)
        verticalLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        verticalLayout.setContentsMargins(10,20,0,0)
        horizontalLayout.addWidget(default_check)

        gLayout.addWidget(image_package,0,0)
        gLayout.addLayout(horizontalLayout,0,1)
        gLayout.addLayout(self.add_line(),1,1)
        return gLayout


    def createClassicLayout(self,last):

        from PyQt5.QtWidgets import QGridLayout, QHBoxLayout, QVBoxLayout
        from PyQt5.QtCore import Qt

        gLayout = QGridLayout()
        horizontalLayout = QHBoxLayout()
        horizontalLayout.setObjectName("horizontalLayout")
        verticalLayout = QVBoxLayout()
        verticalLayout.setObjectName("verticalLayout")
        verticalLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        verticalLayout.setContentsMargins(10,20,0,0)
        horizontalLayout.addLayout(verticalLayout)
        
        image_package = self.createImage('/usr/share/plasma/look-and-feel/lliurex-desktop-classic/contents/previews/preview.png')
        self.classic_name = self.createName(_(self.translations['classiclayout']))
        self.classic_description = self.createDescription(_(self.translations['classiclayoutdescription']))
        classic_check = self.createRadio('classic',False)

        verticalLayout.addWidget(self.classic_name)
        verticalLayout.addWidget(self.classic_description)
        horizontalLayout.addWidget(classic_check)

        gLayout.addWidget(image_package,0,0)
        gLayout.addLayout(horizontalLayout,0,1)
        return gLayout

    def createImage(self,path_image):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtGui import QIcon
        from PyQt5.QtCore import QSize

        label = QLabel()
        label.setText("")
        label.setScaledContents(True)
        label.setPixmap(QIcon(path_image).pixmap(300,169))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label.setSizePolicy(sizePolicy)
        label.setMaximumSize(QSize(300,169))
        label.setObjectName("imagePackage")
        return label

    def createName(self,name):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtGui import QFont

        label_3 = QLabel()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_3.setSizePolicy(sizePolicy)
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        label_3.setFont(font)
        label_3.setObjectName("label_3")
        label_3.setStyleSheet("QLabel{margin-left:5px; }")
        label_3.setText(_(name))
        return label_3

    def createDescription(self,description):
        from PyQt5.QtWidgets import QLabel, QSizePolicy

        label_2 = QLabel()
        label_2.setWordWrap(True)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        label_2.setSizePolicy(sizePolicy)
        label_2.setObjectName("label_2")
        label_2.setStyleSheet("QLabel{margin-left:5px ; color: #666 }")
        label_2.setText(_(description))
        return label_2

    def createRadio(self,layout_selected, selected):
        from PyQt5.QtWidgets import QRadioButton, QSizePolicy
        from PyQt5.QtGui import QFont

        radioButton = QRadioButton()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        radioButton.setSizePolicy(sizePolicy)
        radioButton.setObjectName("checkBox")
        radioButton.setChecked(selected)
        radioButton.clicked.connect(lambda: self.modify_value(layout_selected))
        return radioButton

    def add_line(self):
        from PyQt5.QtWidgets import QVBoxLayout, QWidget, QSizePolicy

        layout = QVBoxLayout()
        line = QWidget()
        line.setFixedHeight(2)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        line.setSizePolicy(sizePolicy)
        line.setStyleSheet("QWidget{background-color: #ccc}")
        line.setObjectName("line")
        layout.addWidget(line)
        layout.setContentsMargins(20,5,0,0)
        return layout
    
    def modify_value(self, layout):
        with open('/run/user/999/ubiquity/ubilliurexlayout','w') as fd:
            fd.write(layout)


class Install(plugin.InstallPlugin):
    
    def install(self, target, progress, *args, **kwargs):
        layout = 'default'
        with open('/run/user/999/ubiquity/ubilliurexlayout') as fd:
            layout = fd.readline().strip()
        os.system('chroot {target} /usr/bin/llx-desktop-layout set {layout}'.format(target=target,layout=layout))

        return plugin.InstallPlugin.install(self, target, progress, *args, **kwargs)
