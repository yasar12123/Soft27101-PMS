from src.ClassDatabaseConnection import DatabaseConnection
from src.ClassUser import User
from src.ClassUserRole import UserRole
from src.ClassProject import Project
from src.ClassProjectTeam import ProjectTeam
from src.ClassTeam import Team
from src.ClassTask import Task
from src.ClassCommunicationLog import CommunicationLog
from src.ClassAttachment import Attachment




# Example usage
if __name__ == '__main__':
    # Create a session
    db = DatabaseConnection()
    session = db.get_session()


    # Get the ID of the team member (replace 1 with the actual ID)
    team_member_username = 'po1'

    # Query all projects for the team member
    # a = Project()
    # projects = a.get_projects_for_team_member(session, team_member_username)
    # for project in projects:
    #     print(project)

    with session() as session:
        query = (
            session.query(Project)
            .join(Project.project_team_members)
            .join(User, ProjectTeam.user_fkey == User.user_pkey)
            .filter(User.username == team_member_username)
        )
        projects = query.all()

        for project in projects:
            print(f"Project Name: {project.name}")
            print(f"Start Date: {project.start_date}")
            print(f"Due Date: {project.due_date}")
            print()  # Print an empty line for separation

