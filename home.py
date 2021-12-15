import sys
from PyQt5.QtWidgets import QPushButton, QLabel, QDoubleSpinBox, QWidget, QHBoxLayout, QMessageBox, QFrame, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QPolygon, QFont
from PyQt5.Qt import Qt
from PyQt5.QtCore import QPoint
from formulas import FORMULAS
from graph import GraphWindow


class MyWidget(QWidget):
    def __init__(self, text, decimals, min=0, max=1000000, default=0):
        super().__init__()
        layout = QHBoxLayout(self)
        self.setStyleSheet("font-size: 16pt; font-family: Futura;")
        self.setLayout(layout)
        self.lbl = QLabel(text=text)
        self.val = QDoubleSpinBox(
            decimals=decimals, minimum=min, maximum=max, value=default)
        layout.addWidget(self.lbl)
        layout.addWidget(self.val)

    def getValue(self):
        if self.val.value() == 0:
            return None
        return float(self.val.value())

    def change_decimals(self, decimals):
        self.val.setDecimals(decimals)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Triangle Calculator")
        self.setFixedSize(800, 600)
        self.decimals = 2
        self.widgets()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        points = [
            QPoint(50, 300),
            QPoint(500, 300),
            QPoint(150, 100)
        ]

        painter.drawPolygon(QPolygon(points))
        points = [
            QPoint(150, 280),
            QPoint(150, 300),
            QPoint(130, 300),
            QPoint(130, 280),
        ]
        painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        painter.drawPolygon(QPolygon(points))
        p = QPainter(self)
        p.setPen(QPen(Qt.black, 5, Qt.DotLine))
        p.drawLine(150, 105, 150, 300)

    def solve_triangle(self):
        A = self.angle_a.getValue()
        B = self.angle_b.getValue()
        C = self.angle_c.getValue()

        a = self.side_a.getValue()
        b = self.side_b.getValue()
        c = self.side_c.getValue()
        decimals = int(self.decimals_spin.getValue())

        x = 0
        for value in [a, b, c, A, B, C]:
            if value != None:
                x += 1
        if x != 3:
            dlg = QMessageBox(
                self, text=f'MUST HAVE EXACTLY 3 VALUES; {x} GIVEN')
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec()
        elif A != None and B != None and C != None:
            dlg = QMessageBox(
                self, text=f'3 ANGLES CANNOT BE GIVEN, ENTER ONE SIDE INSTEAD')
            dlg.setIcon(QMessageBox.Warning)
            dlg.exec()
        elif x == 3:
            values = FORMULAS(a=a, b=b, c=c, A=A, B=B, C=C, decimals=decimals)
            if values == None:
                dlg = QMessageBox(
                    self, text=f'INVALID TRIANGLE')
                dlg.setIcon(QMessageBox.Warning)
                dlg.exec()
                return

            m = GraphWindow(values=values, decimals=decimals)
            m.show()

    def widgets(self):
        clbl = QLabel(self, text="c", font=(QFont("Futura", 24)))
        clbl.move(50, 150)
        blbl = QLabel(self, text="b", font=(QFont("Futura", 24)))
        blbl.move(300, 120)
        albl = QLabel(self, text="a", font=(QFont("Futura", 24)))
        albl.move(250, 320)

        Albl = QLabel(self, text="A", font=(QFont("Futura", 24)))
        Albl.move(140, 60)
        Clbl = QLabel(self, text="C", font=(QFont("Futura", 24)))
        Clbl.move(510, 300)
        Blbl = QLabel(self, text="B", font=(QFont("Futura", 24)))
        Blbl.move(20, 300)

        frm = QFrame(self)
        frm.setFont(QFont("Futura", 15))

        frm.move(0, 375)

        layout = QGridLayout(frm)
        self.angle_a = MyWidget(text="m(∠A):", decimals=self.decimals)
        layout.addWidget(self.angle_a, 0, 0)

        self.angle_b = MyWidget(text="m(∠B):", decimals=self.decimals)
        layout.addWidget(self.angle_b, 0, 1)

        self.angle_c = MyWidget(text="m(∠C):", decimals=self.decimals)
        layout.addWidget(self.angle_c, 0, 2)

        ...

        self.side_a = MyWidget(text="Side Length a:", decimals=self.decimals)
        layout.addWidget(self.side_a, 1, 0)

        self.side_b = MyWidget(text="Side Length b:", decimals=self.decimals)
        layout.addWidget(self.side_b, 1, 1)

        self.side_c = MyWidget(text="Side Length c:", decimals=self.decimals)
        layout.addWidget(self.side_c, 1, 2)

        self.decimals_spin = MyWidget(
            text="Decimals:", decimals=0, min=1, max=7, default=2)

        def decimals_changed(d):
            self.angle_a.change_decimals(d)
            self.angle_b.change_decimals(d)
            self.angle_c.change_decimals(d)

            self.side_a.change_decimals(d)
            self.side_b.change_decimals(d)
            self.side_c.change_decimals(d)

        self.decimals_spin.val.valueChanged.connect(
            lambda: decimals_changed(int(self.decimals_spin.getValue())))
        layout.addWidget(self.decimals_spin, 2, 0)

        button = QPushButton(self, text='SOLVE TRIANGLE')
        button.setFixedSize(150, 50)
        button.setFont(QFont("Futura", 14))
        button.setStyleSheet("""
            background-color: rgb(99, 213, 196);
            color: white;
            border-radius: 10px;
        """)
        button.move(630, 530)
        button.clicked.connect(self.solve_triangle)
