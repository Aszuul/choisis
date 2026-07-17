import sys
from PySide6 import QtCore, QtWidgets, QtGui

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Choisis")
        self.setMinimumSize(900, 500)
        self.resize(1100, 600)

        self.categories = []
        self.add_button = QtWidgets.QPushButton("+")
        self.add_button.setFixedSize(40, 40)
        self.add_button.clicked.connect(self.addCategory)

        self.categories_container = QtWidgets.QWidget()
        self.categories_layout = QtWidgets.QHBoxLayout(self.categories_container)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)
        self.categories_layout.setSpacing(12)

        self.choice_widget = ChoiceWidget()
        self.choice_widget.setFixedWidth(220)
        self.choice_widget.setMinimumHeight(400)
        self.choice_widget.setMaximumWidth(220)

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.widget)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(12)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.categories.append(Category("Enjoyment"))
        self.updateLayout()

    def addCategory(self):
        title = f"Category {len(self.categories) + 1}"
        self.categories.append(Category(title))
        self.updateLayout()

    def updateLayout(self):
        while self.categories_layout.count():
            item = self.categories_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        for category in self.categories:
            self.categories_layout.addWidget(category)

        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self.main_layout.addWidget(self.choice_widget)
        self.main_layout.addWidget(self.categories_container)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 1)
        self.main_layout.setStretch(2, 0)

class ChoiceWidget(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()

        self.classes = ['Warrior','Hunter','Priest','Mage','Monk','Demon Hunter','Evoker','Paladin','Rogue','Shaman','Warlock','Druid','Death Knight']

        self.addItems(self.classes)

        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        
class Category(QtWidgets.QWidget):
    def __init__(self, title):
        super().__init__()
        self.setFixedWidth(220)
        self.setMinimumHeight(320)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        label = QtWidgets.QLineEdit(title)
        label.setMaximumHeight(label.sizeHint().height())
        layout.addWidget(label)

        self.rankings = []
        self.list = CategoryList()
        self.list.setFixedHeight(260)
        layout.addWidget(self.list)


class CategoryList(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.DragDrop)
        self.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        self.setAlternatingRowColors(True)
        # self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def dragEnterEvent(self, event):
        if event.source() is not None and isinstance(event.source(), QtWidgets.QListWidget):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.source() is not None and isinstance(event.source(), QtWidgets.QListWidget):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        source = event.source()
        if source is not None and isinstance(source, QtWidgets.QListWidget):
            item = source.currentItem()
            if item is None:
                event.ignore()
                return

            text = item.text()
            if self.findItems(text, QtCore.Qt.MatchExactly):
                event.ignore()
                return

            self.addItem(text)
            event.acceptProposedAction()
            return

        super().dropEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
