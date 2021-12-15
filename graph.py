from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QWidget, QFrame, QVBoxLayout, QCheckBox, QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from pyqtgraph import PlotWidget, InfiniteLine, mkPen, TextItem
from math import cos, sin, radians
import numpy as np


class GraphWindow(QWidget):
    def __init__(self, values, decimals):
        super().__init__()
        self.values = values
        self.decimals = decimals
        self.setWindowTitle('Graph')
        self.setFixedSize(1250, 700)
        self.setStyleSheet('''
        background-color: rgb(28, 30, 38);
        QLabel {
            font-family; Futura;
            font-size: 16;
            }
        ''')

        self.MAKE_GRAPH()

        ...
        ...
        ...
        toggle_frm = QFrame(self)
        toggle_frm.move(30, 500)
        toggle_frm.setStyleSheet(
            "background-color: transparent; font-family: Futura; font-size: 16pt;")
        l = QVBoxLayout(toggle_frm)
        l.setSpacing(20)

        self.incircle_check = QCheckBox(self, text='Show Incircle')
        self.incircle_check.setStyleSheet('color: rgb(205, 138, 74);')
        self.incircle_check.clicked.connect(self.draw_incircle)
        self.circumcircle_check = QCheckBox(self, text='Show Circumcircle')
        self.circumcircle_check.setStyleSheet('color: rgb(249, 236, 117)')
        self.circumcircle_check.clicked.connect(self.draw_circumcircle)
        self.medians_check = QCheckBox(self, text='Show Medians')
        self.medians_check.setStyleSheet('color: #C54E57')
        self.medians_check.clicked.connect(
            lambda: self.draw_medians(color='#C54E57'))

        l.addWidget(self.incircle_check)
        l.addWidget(self.circumcircle_check)
        l.addWidget(self.medians_check)

        ...
        ...
        ...

        frm = QFrame(self)
        layout = QVBoxLayout(frm)
        layout.setSpacing(10)

        frm.move(800, 25)

        def label_shortcut(text, color):
            if text == None:
                layout.addWidget(QLabel(text='\n\n'))
                return

            for t in text:
                lbl = QLabel(text=t)
                lbl.setStyleSheet(f"""
                color: {color[text.index(t)]};
                font-family: Futura;
                font-size: 14pt;
                """)
                layout.addWidget(lbl)

        text_colors = {
            f"Side Length a: {self.values['a']}": 'rgb(99, 213, 196)',
            f"Side Length b: {self.values['b']}": 'rgb(99, 213, 196)',
            f"Side Length c: {self.values['c']}": 'rgb(99, 213, 196)',

            f"m∠ A: {self.values['A']}°": 'rgb(140, 252, 196)',
            f"m∠ B: {self.values['B']}°": 'rgb(140, 252, 196)',
            f"m∠ C: {self.values['C']}°": 'rgb(140, 252, 196)',

            f"Area: {self.values['area']}": '#EEEADE',
            f"Perimeter: {self.values['perimeter']}": '#EEEADE',
            f"Semiperimeter: {self.values['semiperimeter']}": '#EEEADE',

            f"Inradius: {self.values['inradius']}": 'rgb(205, 138, 74)',
            f"Incenter Coordinates: {(round(self.INCENTER[0], self.decimals), round(self.INCENTER[1], self.decimals))}": 'rgb(205, 138, 74)',

            f"Circumradius: {self.values['circumradius']}": 'rgb(249, 236, 117)',
            f"Circumcenter Coordinates: {(round(self.CIRCUMCENTER[0], self.decimals), round(self.CIRCUMCENTER[1], self.decimals))}": 'rgb(249, 236, 117)',

            f"Height a: {self.values['heights'][0]}": 'pink',
            f"Height b: {self.values['heights'][1]}": 'pink',
            f"Height c: {self.values['heights'][2]}": 'pink',

            f"Median A: {self.values['medians'][0]}": '#C54E57',
            f"Median B: {self.values['medians'][1]}": '#C54E57',
            f"Median C: {self.values['medians'][2]}": '#C54E57',

            f"Angle Classification: {self.values['type_angle']} Triangle": 'rgb(218, 190, 255)',
            f"Side Classification: {self.values['type_side']} Triangle": 'rgb(218, 190, 255)',


        }

        label_shortcut = label_shortcut(
            text=list(text_colors.keys()), color=list(text_colors.values()))

        lbl = QLabel(
            self, text="Press and hold 'Z' to correct zoom and aspect ratio")
        lbl.setStyleSheet(
            "color: #EEEADE; font-family: Futura; font-size: 16pt; background-color: transparent;")
        lbl.move(55, 25)

        self.graph.autoRange()

    def keyPressEvent(self, event):
        if event.key() == 90:
            self.graph.autoRange()

    def MAKE_GRAPH(self):
        self.a_coords = (0, 0)
        self.b_coords = (self.values['c'], 0)

        if self.values['A'] > 90:
            x = (self.values['b'] * cos(radians(180 - self.values['A']))) * -1
            y = self.values['b'] * sin(radians(180 - self.values['A']))
        elif self.values['A'] == 90:
            x = 0
            y = self.values['b']
        elif self.values['A'] < 90:
            x = self.values['b'] * cos(radians(self.values['A']))
            y = self.values['b'] * sin(radians(self.values['A']))

        self.c_coords = (x, y)

        centroid_coords = self.centroid(
            self.a_coords, self.b_coords, self.c_coords)
        vector = (centroid_coords[0] * -1, centroid_coords[1] * -1)

        self.a_coords = self.translate(coords=self.a_coords, vector=vector)
        self.b_coords = self.translate(coords=self.b_coords, vector=vector)
        self.c_coords = self.translate(coords=self.c_coords, vector=vector)

        x_axis = [self.a_coords[0], self.b_coords[0],
                  self.c_coords[0], self.a_coords[0]]
        y_axis = [self.a_coords[1], self.b_coords[1],
                  self.c_coords[1], self.a_coords[1]]

        self.graph = PlotWidget(self)
        self.graph.setBackground((28, 30, 38))
        self.graph.setFixedSize(800, 700)
        self.graph.showGrid(x=True, y=True)
        self.graph.setAspectLocked(1)
        self.graph.addItem(InfiniteLine(
            angle=0, pen=mkPen(color=(90, 90, 94), width=7)))
        self.graph.addItem(InfiniteLine(
            angle=90, pen=mkPen(color=(90, 90, 94), width=7)))

        self.graph.setRange(xRange=[0, 0], yRange=[0, 0])

        pen = mkPen(color=(99, 213, 196), width=10)
        self.graph.plot(x_axis, y_axis, pen=pen)
        self.graph.plot([self.a_coords[0], self.b_coords[0], self.c_coords[0]], [self.a_coords[1], self.b_coords[1], self.c_coords[1]], symbolSize=15,
                        symbolPen=mkPen(color=(180, 252, 194)), symbolBrush=(140, 252, 156))

        ...
        self.INCENTER = self.incenter(
            a=self.a_coords, b=self.b_coords, c=self.c_coords)

        self.CIRCUMCENTER = self.circumcenter(
            a=self.a_coords, b=self.b_coords, c=self.c_coords)

        self.graph.plot([0], [0], symbol='o', symbolPen=(99,
                        213, 196), symbolBrush=(99, 213, 196), symbolSize=20)

        tA = TextItem(text="A: " + str((round(self.a_coords[0], self.decimals), round(self.a_coords[1], self.decimals))),
                      color=(140, 252, 156), anchor=(0, 0))

        tB = TextItem(text="B: " + str((round(self.b_coords[0], self.decimals), round(self.b_coords[1], self.decimals))),
                      color=(140, 252, 156), anchor=(0, 0))

        tC = TextItem(text="C: " + str((round(self.c_coords[0], self.decimals), round(self.c_coords[1], self.decimals))),
                      color=(140, 252, 156), anchor=(0, 1))

        tA.setPos(self.a_coords[0], self.a_coords[1])
        tA.setFont(QFont("Futura", 16))
        tB.setPos(self.b_coords[0], self.b_coords[1])
        tB.setFont(QFont("Futura", 16))
        tC.setPos(self.c_coords[0], self.c_coords[1])
        tC.setFont(QFont("Futura", 16))

        self.graph.addItem(tA)
        self.graph.addItem(tB)
        self.graph.addItem(tC)

        self.graph.plot([0], [0], symbol='+', symbolPen=(99,
                        213, 196), symbolBrush=(99, 213, 196), symbolSize=20)

    def centroid(self, a, b, c):
        x = (a[0] + b[0] + c[0]) / 3
        y = (a[1] + b[1] + c[1]) / 3
        return (x, y)

    def incenter(self, a, b, c):
        x = ((self.values['a'] * a[0]) + (self.values['b'] *
                                          b[0]) + (self.values['c'] * c[0])) / (self.values['perimeter'])

        y = ((self.values['a'] * a[1]) + (self.values['b'] *
                                          b[1]) + (self.values['c'] * c[1])) / (self.values['perimeter'])
        return (x, y)

    def circumcenter(self, a, b, c):
        x = (a[0] * sin(radians(2 * self.values['A']))) + (b[0] * sin(radians(2 *
                                                                              self.values['B']))) + (c[0] * sin(radians(2 * self.values['C'])))
        x = x / (sin(radians(2 * self.values['A'])) + sin(
            radians(2 * self.values['B'])) + sin(radians(2 * self.values['C'])))

        y = (a[1] * sin(radians(2 * self.values['A']))) + (b[1] * sin(radians(2 *
                                                                              self.values['B']))) + (c[1] * sin(radians(2 * self.values['C'])))
        y = y / (sin(radians(2 * self.values['A'])) + sin(
            radians(2 * self.values['B'])) + sin(radians(2 * self.values['C'])))
        return (x, y)

    def translate(self, coords, vector):
        return (coords[0] + vector[0], coords[1] + vector[1])

    def draw_circumcircle(self):

        def draw_circle(center, radius, color):
            r = radius
            h, k = center
            x = np.linspace(h - r, h + r, 1000)
            y = k + ((r**2 - (x-h)**2))**(1/2)
            pen = mkPen(color, width=3, style=QtCore.Qt.DashDotLine)
            self.c_line0 = self.graph.plot(x, y, pen=pen)
            y = k - ((r**2 - (x-h)**2))**(1/2)
            self.c_line1 = self.graph.plot(x, y, pen=pen)
            self.c_line2 = self.graph.plot([h], [k], symbol='o',
                                           symbolPen=color, symbolBrush=color)
            self.c_line3 = self.graph.plot([h, h+r], [k, k], pen=pen)

        if self.circumcircle_check.isChecked() == True:
            draw_circle(center=self.CIRCUMCENTER,
                        radius=self.values['circumradius'], color=(249, 236, 117))
        else:
            self.graph.removeItem(self.c_line0)
            self.graph.removeItem(self.c_line1)
            self.graph.removeItem(self.c_line2)
            self.graph.removeItem(self.c_line3)

    def draw_incircle(self):
        def draw_circle(center, radius, color):
            r = radius
            h, k = center
            x = np.linspace(h - r, h + r, 1000)
            y = k + ((r**2 - (x-h)**2))**(1/2)
            pen = mkPen(color, width=3, style=QtCore.Qt.DashDotLine)
            self.i_line0 = self.graph.plot(x, y, pen=pen)
            y = k - ((r**2 - (x-h)**2))**(1/2)
            self.i_line1 = self.graph.plot(x, y, pen=pen)
            self.i_line2 = self.graph.plot([h], [k], symbol='o',
                                           symbolPen=color, symbolBrush=color)
            self.i_line3 = self.graph.plot([h, h+r], [k, k], pen=pen)

        if self.incircle_check.isChecked() == True:
            draw_circle(
                center=self.INCENTER, radius=self.values['inradius'], color=(205, 138, 74))
        else:
            self.graph.removeItem(self.i_line0)
            self.graph.removeItem(self.i_line1)
            self.graph.removeItem(self.i_line2)
            self.graph.removeItem(self.i_line3)

    def draw_medians(self, color):
        if self.medians_check.isChecked() == True:
            midpoint_a_x = (self.b_coords[0] + self.c_coords[0])/2
            midpoint_a_y = (self.b_coords[1] + self.c_coords[1])/2
            pen = mkPen(color, width=3, style=QtCore.Qt.DashLine)
            self.m_line0 = self.graph.plot([self.a_coords[0], midpoint_a_x], [
                self.a_coords[1], midpoint_a_y], pen=pen)

            midpoint_b_x = (self.a_coords[0] + self.c_coords[0])/2
            midpoint_b_y = (self.a_coords[1] + self.c_coords[1])/2
            pen = mkPen(color, width=3, style=QtCore.Qt.DashLine)
            self.m_line1 = self.graph.plot([self.b_coords[0], midpoint_b_x], [
                self.b_coords[1], midpoint_b_y], pen=pen)

            midpoint_c_x = (self.b_coords[0] + self.a_coords[0])/2
            midpoint_c_y = (self.b_coords[1] + self.a_coords[1])/2
            pen = mkPen(color, width=3, style=QtCore.Qt.DashLine)
            self.m_line2 = self.graph.plot([self.c_coords[0], midpoint_c_x], [
                self.c_coords[1], midpoint_c_y], pen=pen)
        else:
            self.graph.removeItem(self.m_line0)
            self.graph.removeItem(self.m_line1)
            self.graph.removeItem(self.m_line2)
