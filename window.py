import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_StaticContents)
        h = 250
        w = 250
        self.myPenWidth = 5
        self.myPenColor = Qt.black
        self.image = QImage(w, h, QImage.Format_RGB32)
        self.path = QPainterPath()
        self.clearImage()

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)
        self.update()

    def saveImage(self, fileName, fileFormat):
        im = self.image.scaled(28, 28, Qt.IgnoreAspectRatio)
        im.save(fileName, fileFormat)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def mousePressEvent(self, event):
        self.path.moveTo(event.pos())

    def mouseMoveEvent(self, event):
        self.path.lineTo(event.pos())
        p = QPainter(self.image)
        p.setPen(QPen(self.myPenColor,
                      self.myPenWidth, Qt.SolidLine, Qt.RoundCap,
                      Qt.RoundJoin))
        p.drawPath(self.path)
        p.end()
        self.update()

    def sizeHint(self):
        return QSize(100, 100)


class MyWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setLayout(QVBoxLayout())
        label = QLabel(self)
        drawer = Drawer(self)
        drawer.newPoint.connect(lambda p: label.setText('Coordinates: ( %d : %d )' % (p.x(), p.y())))
        self.layout().addWidget(label)
        self.layout().addWidget(drawer)


class MainWind(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        drawer = Drawer()
        exitAction = QAction(QIcon('web.png'), 'Exit', self)
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)
        probab = QLabel('Достоверность определения: ')
        answer = QLabel('Вы нарисовали цифру: ')
        title = QLabel('Нарисуйте цифру в области справа')
        delpict = QPushButton('Очистить', self)
        delpict.clicked.connect(lambda: drawer.clearImage())
        photo = QPushButton('Обработать изображение', self)
        photo.clicked.connect(lambda: drawer.saveImage("image.png", "PNG"))


        grid = QGridLayout()
        grid.addWidget(title, 1, 0)
        grid.addWidget(probab, 2, 0)
        grid.addWidget(answer, 3, 0)
        grid.addWidget(delpict, 4, 0)
        grid.addWidget(photo, 5, 0)
        grid.addWidget(drawer, 1, 1, 5, 1)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(grid)

        self.setGeometry(700, 400, 550, 310)
        self.setWindowTitle('Main Window')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWind()
    ex.show()
    sys.exit(app.exec_())


