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

        self.clear_all_button = QtWidgets.QPushButton("Clear All")
        self.clear_all_button.clicked.connect(self.clearAllCategories)

        self.categories_container = QtWidgets.QWidget()
        self.categories_layout = QtWidgets.QHBoxLayout(self.categories_container)
        self.categories_layout.setContentsMargins(0, 0, 0, 0)
        self.categories_layout.setSpacing(12)

        self.choice_widget = ChoiceWidget()
        self.choice_widget.setFixedWidth(220)
        self.choice_widget.setMinimumHeight(400)
        self.choice_widget.setMaximumWidth(220)

        self.rank_widget = rankWidget()
        self.choice_controls = ChoiceControls(self.choice_widget, self)

        self.left_container = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QVBoxLayout(self.left_container)
        self.left_layout.setContentsMargins(0, 0, 0, 0)
        self.left_layout.setSpacing(12)
        self.left_layout.addWidget(self.choice_controls)
        self.left_layout.addWidget(self.choice_widget)
        self.left_layout.addWidget(self.rank_widget)

        self.widget = QtWidgets.QWidget()
        self.setCentralWidget(self.widget)
        self.main_layout = QtWidgets.QHBoxLayout(self.widget)
        self.main_layout.setContentsMargins(12, 12, 12, 12)
        self.main_layout.setSpacing(12)
        self.main_layout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)

        self.categories.append(Category("Enjoyment", self.choice_widget, self))
        self.updateLayout()

    def addCategory(self):
        title = f"Category {len(self.categories) + 1}"
        self.categories.append(Category(title, self.choice_widget, self))
        self.updateLayout()

    def clearAllCategories(self):
        for category in self.categories:
            category.list.clear()
            category.update_rankings()
        self.choice_widget.refresh_missing_highlight(self.categories)
        self.rank_widget.update_ranking(self.categories, self.choice_widget)

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

        self.main_layout.addWidget(self.left_container)
        self.main_layout.addWidget(self.categories_container)
        self.main_layout.addWidget(self.add_button)
        self.main_layout.addWidget(self.clear_all_button)
        self.main_layout.setStretch(0, 0)
        self.main_layout.setStretch(1, 1)
        self.main_layout.setStretch(2, 0)
        self.main_layout.setStretch(3, 0)

        self.choice_widget.refresh_missing_highlight(self.categories)
        self.rank_widget.update_ranking(self.categories, self.choice_widget)

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

    def add_item(self, text):
        if not text.strip():
            return

        if self.findItems(text, QtCore.Qt.MatchExactly):
            return

        self.addItem(text)
        if hasattr(self, "main_window") and self.main_window is not None:
            self.refresh_missing_highlight(self.main_window.categories)
            self.main_window.rank_widget.update_ranking(self.main_window.categories, self)

    def refresh_missing_highlight(self, categories):
        for index in range(self.count()):
            item = self.item(index)
            value = item.data(QtCore.Qt.UserRole) or item.text()
            present_in_all = True

            if not categories:
                present_in_all = False
            else:
                for category in categories:
                    if not self._is_present_in_list(value, category.list):
                        present_in_all = False
                        break

            if present_in_all:
                item.setBackground(QtGui.QColor())
            else:
                item.setBackground(QtGui.QColor("#f8b4b4"))

    def _is_present_in_list(self, value, list_widget):
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            if item is None:
                continue
            existing_value = item.data(QtCore.Qt.UserRole) or item.text()
            if existing_value == value:
                return True
        return False
        
class Category(QtWidgets.QWidget):
    def __init__(self, title, choice_widget, main_window):
        super().__init__()
        self.setFixedWidth(220)
        self.setMinimumHeight(320)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.choice_widget = choice_widget
        self.main_window = main_window

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        header_layout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLineEdit(title)
        label.setMaximumHeight(label.sizeHint().height())
        header_layout.addWidget(label)

        delete_button = QtWidgets.QPushButton("×")
        delete_button.setFixedSize(28, 28)
        delete_button.clicked.connect(self.delete_category)
        header_layout.addWidget(delete_button)
        layout.addLayout(header_layout)

        self.rankings = []
        self.list = CategoryList(self, choice_widget)
        self.list.setFixedHeight(260)
        layout.addWidget(self.list)

    def update_rankings(self):
        values = []
        for index in range(self.list.count()):
            item = self.list.item(index)
            if item is None:
                continue
            value = item.data(QtCore.Qt.UserRole) or item.text()
            values.append(value)

        self.rankings = values

        for index, value in enumerate(values):
            item = self.list.item(index)
            if item is None:
                continue
            item.setData(QtCore.Qt.UserRole, value)
            item.setText(f"{value}")

        if self.choice_widget is not None and self.main_window is not None:
            self.choice_widget.refresh_missing_highlight(self.main_window.categories)
            self.main_window.rank_widget.update_ranking(self.main_window.categories, self.choice_widget)

    def delete_category(self):
        if self.main_window is None:
            return

        self.main_window.categories = [category for category in self.main_window.categories if category is not self]
        self.main_window.updateLayout()


class CategoryList(QtWidgets.QListWidget):
    def __init__(self, category, choice_widget):
        super().__init__()
        self.category = category
        self.choice_widget = choice_widget
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(QtCore.Qt.DropAction.MoveAction)
        self.setAlternatingRowColors(True)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)

    def _contains_value(self, value):
        for index in range(self.count()):
            item = self.item(index)
            if item is None:
                continue
            existing = item.data(QtCore.Qt.UserRole) or item.text()
            if existing == value:
                return True
        return False

    def remove_selected(self):
        current_row = self.currentRow()
        if current_row >= 0:
            self.takeItem(current_row)
            self.category.update_rankings()

    def delete_selected(self):
        current_row = self.currentRow()
        if current_row >= 0:
            self.takeItem(current_row)
            self.category.update_rankings()

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
        if event.source() is self:
            super().dropEvent(event)
            self.category.update_rankings()
            return

        if event.source() is not None and isinstance(event.source(), QtWidgets.QListWidget):
            item = event.source().currentItem()
            if item is None:
                event.ignore()
                return

            text = item.text()
            if self._contains_value(text):
                event.ignore()
                return

            new_item = QtWidgets.QListWidgetItem(text)
            new_item.setData(QtCore.Qt.UserRole, text)
            self.addItem(new_item)
            self.category.update_rankings()
            event.acceptProposedAction()
            return

        event.ignore()

class ChoiceControls(QtWidgets.QWidget):
    def __init__(self, choice_widget, main_window):
        super().__init__()
        self.choice_widget = choice_widget
        self.main_window = main_window

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.input = QtWidgets.QLineEdit()
        self.input.setPlaceholderText("Add item")
        self.input.returnPressed.connect(self.add_item)
        layout.addWidget(self.input)

        add_button = QtWidgets.QPushButton("Add")
        add_button.clicked.connect(self.add_item)
        layout.addWidget(add_button)

        delete_button = QtWidgets.QPushButton("Delete")
        delete_button.clicked.connect(self.delete_selected)
        layout.addWidget(delete_button)

    def add_item(self):
        self.choice_widget.add_item(self.input.text())
        self.input.clear()
        if self.main_window is not None:
            self.choice_widget.refresh_missing_highlight(self.main_window.categories)
            self.main_window.rank_widget.update_ranking(self.main_window.categories, self.choice_widget)

    def delete_selected(self):
        current_row = self.choice_widget.currentRow()
        if current_row >= 0:
            self.choice_widget.takeItem(current_row)
            if self.main_window is not None:
                self.choice_widget.refresh_missing_highlight(self.main_window.categories)
                self.main_window.rank_widget.update_ranking(self.main_window.categories, self.choice_widget)

class rankWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(220)
        self.setMinimumHeight(120)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(6)

        self.label = QtWidgets.QLabel("Rankings")
        self.label.setWordWrap(True)
        layout.addWidget(self.label)

    def update_ranking(self, categories, choice_widget):
        rankings = []
        for index in range(choice_widget.count()):
            item = choice_widget.item(index)
            value = item.data(QtCore.Qt.UserRole) or item.text()
            present_in_all = True
            total_index = 0

            for category in categories:
                category_index = None
                for list_index in range(category.list.count()):
                    list_item = category.list.item(list_index)
                    if list_item is None:
                        continue
                    existing_value = list_item.data(QtCore.Qt.UserRole) or list_item.text()
                    if existing_value == value:
                        category_index = list_index
                        break

                if category_index is None:
                    present_in_all = False
                    break

                total_index += category_index

            if present_in_all:
                rankings.append((total_index, value))

        rankings.sort(key=lambda entry: (entry[0], entry[1]))

        if not rankings:
            text = "No items appear in all categories."
        else:
            lines = [f"{rank}. {value} (sum {score})" for rank, (score, value) in enumerate(rankings, start=1)]
            text = "\n".join(lines)

        self.label.setText(text)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
