# def plot_project_gantt_chart(self):
#     p = Project()
#     projects = p.get_projects_for_team_member(self.session, self.activeUserInstance.username)
#
#     # data for plotting
#     project_names = [project.name for project in projects]
#     start_dates = [project.start_date for project in projects]
#     due_dates = [project.due_date for project in projects]
#
#     # Plot Gantt chart
#     fig, ax = plt.subplots(figsize=(5, 3))
#     for idx, project_name in enumerate(project_names):
#         print(type(due_dates[idx]))
#         ax.barh(project_name, due_dates[idx], left=start_dates[idx], color='skyblue')
#     ax.set_xlabel('Date')
#     ax.set_ylabel('Project')
#     ax.set_title('Gantt Chart')
#     ax.grid(True)
#     plt.tight_layout()
#
#     # Embed Gantt chart
#     canvas = FigureCanvas(fig)
#     layout = QVBoxLayout(self.projectPlotFrame)
#     layout.addWidget(canvas)

# def plot_project_pie_charts(self):
#     p = Project()
#     projects = p.get_projects_for_team_member(self.session, self.activeUserInstance.username)
#
#     # Data for plotting
#     completed_tasks = sum(1 for project in projects if project.status == 'Completed')
#     all_tasks = len(projects)
#     project_completion_percentage = completed_tasks / all_tasks * 100
#
#     # Plot pie charts
#     fig, axs = plt.subplots(1, 3, figsize=(8, 4))
#
#     # Pie chart for completed tasks
#     axs[0].pie([completed_tasks, all_tasks - completed_tasks], labels=['Completed', 'Not Completed'],
#                autopct='%1.1f%%')
#     axs[0].set_title('Completed Tasks')
#
#     # Horizontal bar chart for all tasks
#     categories = ['Not Started', 'Completed']
#     counts = [all_tasks - completed_tasks, completed_tasks]
#     axs[1].barh(categories, counts, color=['blue', 'green'])
#     axs[1].set_xlabel('Number of Tasks')
#     axs[1].set_title('All Tasks')
#
#     # Pie chart for project completion
#     axs[2].pie([project_completion_percentage, 100 - project_completion_percentage],
#                labels=['Completed', 'Remaining'], autopct='%1.1f%%')
#     axs[2].set_title('Project Completion')
#
#     fig.tight_layout()
#
#     # Embed pie charts
#     canvas = FigureCanvas(fig)
#     layout = QVBoxLayout(self.statsFrame)
#     layout.addWidget(canvas)
#
#     # Set size policy to automatically adjust size
#     self.statsFrame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
#     canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
