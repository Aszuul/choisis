from pyexpat import model
import sys
from PySide6 import QtCore, QtWidgets, QtGui

# main window class
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choice and Category Manager")
        self.setGeometry(100, 100, 800, 600)

        # main layout
        self.central_widget = QtWidgets.QWidget()
        self.outerlayout = QtWidgets.QVBoxLayout(self.central_widget)
        self.innerlayout = QtWidgets.QHBoxLayout()

        # choice list
        self.choice_list_widget = ChoiceListWidget()
        self.innerlayout.addWidget(self.choice_list_widget)
        
        # category list
        self.category_list_widget = Categories()
        self.innerlayout.addWidget(self.category_list_widget)

        # add category button
        self.add_category_button = QtWidgets.QPushButton("Add Category")
        self.innerlayout.addWidget(self.add_category_button)
        
        self.outerlayout.addLayout(self.innerlayout)
        
        # ranking field
        self.ranking_field = RankingField()
        self.outerlayout.addWidget(self.ranking_field)
        
        self.setCentralWidget(self.central_widget)

# choice list with entry field
# each item is a widget with label and delete button
class ChoiceListWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        # entry field
        self.entry_field = QtWidgets.QLineEdit()
        self.layout.addWidget(self.entry_field)

        # list widget
        self.list_widget = QtWidgets.QListWidget()
        self.classes = ['Warrior','Hunter','Priest','Mage','Monk','Demon Hunter','Evoker','Paladin','Rogue','Shaman','Warlock','Druid','Death Knight']
        for cls in self.classes:
            item = QtWidgets.QListWidgetItem(cls)
            self.list_widget.addItem(item)
        self.list_widget.setDragEnabled(True)
        self.list_widget.setDragDropMode(QtWidgets.QListWidget.InternalMove)
              
        self.layout.addWidget(self.list_widget)
        
        # connect entry field to add choice
        self.entry_field.returnPressed.connect(self.add_choice)

    def add_choice(self):
        choice_text = self.entry_field.text()
        if choice_text:
            item = QtWidgets.QListWidgetItem(choice_text)
            self.list_widget.addItem(item)
            self.entry_field.clear()

# category list, able to accept drops from choice list and drag out to remove.
class Categories(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.categories = []
        self.setLayout(QtWidgets.QHBoxLayout())
        self.categories.append(CategoryView("Fun"))
        for category in self.categories:
            self.layout().addWidget(category)

class CategoryView(QtWidgets.QWidget):
    def __init__(self, name="Category"):
        super().__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.label = QtWidgets.QLineEdit(name)
        self.list_widget = CategoryListWidget()
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.list_widget)
        self.setAcceptDrops(True)


class CategoryListWidget(QtWidgets.QListWidget):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QListWidget.DragDropMode.DragDrop)

    def dropEvent(self, event):
        if event.source() == self:
            event.setDropAction(QtCore.Qt.DropAction.MoveAction)
            super().dropEvent(event)
        else: 
            model = QtGui.QStandardItemModel()
            model.dropMimeData(event.mimeData(), QtCore.Qt.DropAction.CopyAction, 0,0, QtCore.QModelIndex())
            text = model.item(0, 0).text()
            if self.findItems(text, QtCore.Qt.MatchFlag.MatchExactly):
                event.ignore()
            else:
                super().dropEvent(event)

# button on right to add new category.

# ranking field below that shows the current rank of any choices that appear in all categories.
class RankingField(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.setText("Current Rank: N/A")

    def update_rank(self, rank):
        self.setText(f"Current Rank: {rank}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())