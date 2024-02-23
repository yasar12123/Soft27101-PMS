from PyQt6.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget, QLineEdit


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Create a combo box
        self.combo_box = QComboBox()
        self.combo_box.setEditable(True)  # Allow editing text
        #self.combo_box.lineEdit().textChanged.connect(
          #  self.filter_items)  # Connect text changed signal to filter function
        layout.addWidget(self.combo_box)

        # Add some items to the combo box
        items = ['Apple', 'Banana', 'Orange', 'Grapes', 'Pineapple']
        self.original_items = items.copy()  # Save original items
        self.combo_box.addItems(items)

    # def filter_items(self, text):
    #     # Filter the items based on the entered text
    #     self.combo_box.clear()
    #     for item in self.original_items:
    #         if text.lower() in item.lower():
    #             self.combo_box.addItem(item)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
