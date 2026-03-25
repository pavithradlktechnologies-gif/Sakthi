from .views import *
from django.urls import path


urlpatterns = [
    path("dashboard",dashboard,name="dashboard"),
    path('admin_login',admin_login, name='admin_login'),
    path('admin_logout',admin_logout,name="admin_logout"),
    path('update-receiver-email',update_receiver_email, name='update_receiver_email'),
    path('test-500/', trigger_error,name='trigger_error'),

    # Video section
    path("video",video,name="video"),
    path('change_video/<int:id>',change_video,name="change_video"),

    # Project section
    path('create_project',create_project,name="create_project"),
    path('edit_project/<int:pk>',edit_project,name="edit_project"),
    path('projects_list',projects_list,name="projects_list"),
    path('delete_project/<int:id>',delete_project,name="delete_project"),
    path('project_enquiry',project_enquiry,name="project_enquiry"),
    path('edit_project_enquiry/<int:pk>',edit_project_enquiry,name="edit_project_enquiry"),
    path('delete_project_enquiry/<int:id>',delete_project_enquiry,name="delete_project_enquiry"),
    path('update-project-order/',update_project_order, name='update_project_order'),
    path('download-enquiries-excel/', download_enquiries_excel, name='download_enquiries_excel'),


    # blog

    path('blog_list',blog_list,name="blog_list"),
    path('blog_create',blog_create,name='blog_create'),
    path("blog_edit/<int:id>",blog_edit,name="blog_edit"),
    path("blog_delete/<int:id>",blog_delete,name="blog_delete"),


    # Carrer

    path('job_list',job_list,name="job_list"),
    path('create_job',create_job,name="create_job"),
    path('edit_job/<int:id>',edit_job,name="edit_job"),
    path('delete_job/<int:id>',delete_job,name="delete_job"),
    path('job_applications',job_applications,name="job_applications"),
    path(
        "download-job-applications/",
        download_job_applications_excel,
        name="download_job_applications_excel"
    ),

    #Contact Details
    path('contact_details',contact_details,name="contact_details"),
    path('download-contacts/', download_contacts_excel, name='download_contacts_excel'),
    path('delete-contact/<int:id>/',delete_contact, name='delete_contact'),

]




