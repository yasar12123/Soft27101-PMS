from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment

from PyQt6.QtWidgets import QApplication, QMainWindow
from generated.ProjectWindow import Ui_ProjectWindow

import sys

class ProjectWindow(QMainWindow, Ui_ProjectWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def populate_table(self):
        # Establish a connection to your database
        engine = create_engine("sqlite:///your_database.db")  # Replace with your database connection
        Session = sessionmaker(bind=engine)
        session = Session()

        # Fetch data from the database
        data = session.query(YourTable).all()  # Replace YourTable with your SQLAlchemy model

        # Populate the table with data
        self.tableWidget.setRowCount(len(data))
        for row, item in enumerate(data):
            self.tableWidget.setItem(row, 0,
                                     QTableWidgetItem(str(item.column1)))  # Replace column1 with your column names
            self.tableWidget.setItem(row, 1, QTableWidgetItem(str(item.column2)))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(item.column3)))

        # Close the session
        session.close()





def main():
    app = QApplication(sys.argv)
    window = ProjectWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()