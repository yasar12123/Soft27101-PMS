from PyQt6.QtWidgets import QApplication, QComboBox

app = QApplication([])

combo_box = QComboBox()

# Add text directly to the combo box
combo_box.addItem("Your current text")

# Disable the selection for this item
combo_box.model().item(0).setEnabled(False)

combo_box.show()
app.exec()
