import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from test import testing
from mnist_trainedCNN import learner

class Drawer(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_StaticContents)
        h = 250
        w = 250
        self.myPenWidth = 20
        self.myPenColor = Qt.black
        self.image = QImage(w, h, QImage.Format_Grayscale8)
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

    def saveImage(self):
        im = self.image.scaled(28, 28, Qt.IgnoreAspectRatio)
        return im

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
        self.testthread = TestingThread(self)
        self.learnthread = LearnThread(self)

    def initUI(self):
        drawer = Drawer()
        exitAction = QAction('Выход', self)
        exitAction.triggered.connect(qApp.quit)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(exitAction)
        probab = QLabel('Достоверность определения: ')
        prr = QLabel(' ')
        answer = QLabel('Вы нарисовали цифру: ')
        title = QLabel('Нарисуйте цифру в области справа')
        delpict = QPushButton('Очистить', self)
        delpict.clicked.connect(lambda: drawer.clearImage())
        photo = QPushButton('Обработать изображение', self)
        photo.clicked.connect(lambda: self.recognition(drawer, answer, prr))
        learning = QPushButton('Обучить сеть', self)
        learning.clicked.connect(lambda: self.learn())


        grid = QGridLayout()
        grid.addWidget(title, 1, 0)
        grid.addWidget(probab, 3, 0)
        grid.addWidget(prr, 4, 0)
        grid.addWidget(answer, 2, 0)
        grid.addWidget(delpict, 5, 0)
        grid.addWidget(photo, 6, 0)
        grid.addWidget(learning, 7, 0)
        grid.addWidget(drawer, 1, 1, 7, 1)
        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(grid)

        self.setGeometry(700, 400, 550, 310)
        self.setWindowTitle('DigitRecognizer')
        self.setWindowIcon(QIcon('web.jpg'))

    def recognition(self, drawer, answer, prr):
        file = drawer.saveImage()
        self.testthread.file = file
        self.testthread.answer = answer
        self.testthread.prr = prr
        try:
            self.testthread.start()
        except OSError:
            QMessageBox.critical(self, "Ошибка", "Нейросеть не обучена!", QMessageBox.Ok)

    def learn(self):
        self.learnthread.learn = learner()
        self.learnthread.start()
        QMessageBox.information(self, 'Поздравляем!', "Сеть обучена!")

    def cleanup(self):
        if self.testthread:
            self.testthread.requestInterruption()
            self.testthread.exit()
        if self.learnthread:
            self.learnthread.requestInterruption()
            self.learnthread.exit()




class TestingThread(QThread):

    action = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.file = None
        self.answer = None
        self.prr = None

    def run(self):
        self.action.emit(True)
        ans, pr = testing(self.file)
        self.answer.setText('Вы нарисовали цифру: ' + str(ans))
        self.prr.setText(str(pr))
        self.action.emit(False)


class LearnThread(QThread):

    action = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent)
        self.learn = None

    def run(self):
        self.action.emit(True)
        self.learn()

        self.action.emit(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWind()
    ex.show()
    sys.exit(app.exec_())


