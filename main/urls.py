from django.urls import path
from . import views

urlpatterns= [
    path('', views.display_login_and_register_page),

    #create and login
    path('create', views.create_user),
    path('login', views.login),
    #dashboard
    path('dashboard', views.display_dashboard_page),

    #job page
    path("job/new", views.create_job_page),
    #job action
    path("job/create", views.create_job_action),

    #edit job page
    path("jobs/edit/<int:job_id>", views.edit_job_page),
    path("jobs/edit/<int:job_id>/update", views.edit_job_action),

    #view job page
    path("jobs/<int:job_id>", views.view_job_page),
    #DELETE
    path("jobs/<int:job_id>/destroy", views.delete),
]