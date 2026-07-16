import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

# class MyWidget(QtWidgets.QWidget):
#     def __init__(self):
#         super().__init__()

#         self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

#         self.button = QtWidgets.QPushButton("Click me!")
#         self.text = QtWidgets.QLabel("Hello World",
#                                      alignment=QtCore.Qt.AlignCenter)

#         self.layout = QtWidgets.QVBoxLayout(self)
#         self.layout.addWidget(self.text)
#         self.layout.addWidget(self.button)

#         self.button.clicked.connect(self.magic)

# @QtCore.Slot()
# def magic(self):
#     self.text.setText(random.choice(self.hello))

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Choisis")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(ChoiceWidget())
        layout.addWidget(Category())

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

class ChoiceWidget(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()

        self.classes = ['Warrior','Hunter','Priest','Mage','Monk','Demon Hunter','Evoker','Paladin','Rogue','Shaman','Warlock','Druid','Death Knight']

        self.addItems(self.classes)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        # self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        

class Category(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()

        self.rankings = []
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
