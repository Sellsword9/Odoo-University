{
  "name": "University",
  "summary": "University Management System",
  "description": "University Management System",
  "author": "Yeray Romero",
  
  "application": True,
  
  "data": [
    "views/enrolls_kanban.xml",
    "views/notes_kanban.xml",
    "views/departments_kanban.xml",
    "views/departments_view.xml",
    "views/professors_kanban.xml",
    "views/professors_view.xml",
    "views/subjects_kanban.xml",
    "views/subjects_view.xml",
    "views/dossier_graph.xml",
    "views/dossier_pivot.xml",
    "views/students_kanban.xml",
    "views/students_view.xml",
    "reports/student_report.xml",
    "reports/ir.actions_report.xml",
    "reports/email_template_student.xml",
    "views/university_action.xml",
    "views/university_kanban.xml",
    "views/university_view.xml",
    "views/root_menu.xml",
    "security/ir.model.access.csv"
    ],
  "depends": [
    "base",
    "mail",
    "base_setup"
    ],
    "installable": True,
    }
