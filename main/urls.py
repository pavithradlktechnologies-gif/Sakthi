from django.urls import path
from .views import *

urlpatterns = [
    path("",index,name="index"),
    path("about",about,name="about"),
    path("properties",properties,name="properties"),
    path("view_properties/<int:id>",view_properties,name="view_properties"),
    path("services",services,name="services"),
    path("blogs",blogs,name="blogs"),
    path('view_blog/<int:id>',view_blog,name="view_blog"),
    path("new_development",new_development,name="new_development"),
    path("contact_us",contact_us,name="contact_us"),

    path("careers",careers,name="careers"),
    path("apply_job/<int:job_id>/", apply_job, name="apply_job"),
]
