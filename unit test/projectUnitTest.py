from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment
from src.ClassEmail import EmailSender
import unittest
from datetime import datetime


class TestProjectMethods(unittest.TestCase):

    def __init__(self, methodName='runTest', userInstance=None, projectPkey=None, setName='Test Project', setDesc='Test project Desc',
                 setStatus='Not Started', setStartDate=datetime.now(), setDueDate=datetime.now(), setProjectProgress=0, invalidDueDate=None):
        super(TestProjectMethods, self).__init__(methodName)
        self.dbCon = DatabaseConnection()
        self.session = self.dbCon.get_session()
        self.userInstance = userInstance
        self.projectPkey = projectPkey
        self.setName = setName
        self.setDesc = setDesc
        self.setStatus = setStatus
        self.setStartDate = setStartDate
        self.setDueDate = setDueDate
        self.setProjectProgress = setProjectProgress
        self.invalidDueDate = invalidDueDate

    def setUp(self):
        # Initialize a project instance for testing
        self.project = Project()

    def tearDown(self):
        # Clean up after each test
        pass

    def test_add_project_successful(self):
        # Test adding a new project successfully
        result = self.project.add_project(self.session)
        self.assertEqual(result, 'successful')

    def test_add_project_empty_fields(self):
        # Test adding a project with empty fields
        self.project.name = ''
        result = self.project.add_project(self.session)
        self.assertEqual(result, 'the field Project Name can not be empty')


if __name__ == '__main__':
    unittest.main()
