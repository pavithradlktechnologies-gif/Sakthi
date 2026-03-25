from django.shortcuts import render, redirect, get_object_or_404
from admin_dashboard.models import *
from collections import defaultdict
from .forms import *
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime
from django.utils import timezone

import os
import ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def index(request):
    data = Project.objects.all().order_by('order')[:6]
    blogs = BlogPost.objects.all().order_by('-id')[:3]
    return render(request,"main/index.html",{'data':data,'blogs':blogs})


def about(request):
    return render(request,"main/about.html")


def properties(request):
    data = Project.objects.all()
    return render(request,"main/properties.html",{'data':data})


def view_properties(request, id):
    data = get_object_or_404(Project, id=id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        budget = request.POST.get("budget")

        Project_Enquiry.objects.create(
            project=data,
            full_name=full_name,
            email=email,
            mobile_number=mobile,
            budget=budget
        )
        try:
            subject = 'Enquiry Received - Sakthi Property'
            from_email = 'pavithra.dlktechnologies@gmail.com' # Verified email inga kudunga
            to_email = [email]

            context = {
                'full_name': full_name,
                'project_name': data.project_name, # Model-la project_name nu irukka nu check pannunga
                'budget': budget,
                'enquiry_date': datetime.now().strftime("%d-%m-%Y"),
                'mobile_number': mobile,
                'email': email,
                'message': "", # View properties form-la message illana empty-ah vidalam
            }

            html_content = render_to_string('main/enquiry_email.html', context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
        except Exception as e:
            print(f"Enquiry Email Error: {e}")

        return redirect("view_properties", id=id)
   

    amenities = Amenity.objects.filter(project=data)
    floor_plans = FloorPlan.objects.filter(project=data)
    gallery = Gallery.objects.filter(project=data)
    advantages = data.location_advantages.select_related('category').all().order_by('category__order')

    grouped_advantages = defaultdict(list)
    for adv in advantages:
        grouped_advantages[adv.category].append(adv)

    return render(request, "main/view_properties.html", {
        'data': data,
        'amenities': amenities,
        'floor_plans': floor_plans,
        'gallery': gallery,
        'advantages': advantages,
        'grouped_advantages': dict(grouped_advantages)
    })


def services(request):
    return render(request,"main/services.html")


def blogs(request):
    blogs = BlogPost.objects.all()
    return render(request,"main/blogs.html",{'blogs':blogs})


def view_blog(request,id):
    blog = BlogPost.objects.get(id=id)
    return render(request,"main/view_blog.html",{'blog':blog})


def new_development(request):
    datas = Project.objects.filter(project_status="up_comming")
    return render(request,"main/new_development.html",{'datas':datas})

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            phone = form.cleaned_data.get('phone')
            message = form.cleaned_data.get('message')
            project_obj = form.cleaned_data.get('project')

            Project_Enquiry.objects.create(
                full_name=name,
                email=email,
                mobile_number=phone,
                message=message,
                project=project_obj,
                budget="N/A"
            )

            try:
                subject = 'Thank You for Reaching Out! - Sakthi Property'
                from_email = 'pavithra.dlktechnologies@gmail.com'
                to_email = [email]

                context = {
                    'name': name,
                    'project_name': str(project_obj) if project_obj else "General Enquiry",
                    'email': email,
                    'phone': phone,
                    'message': message,
                    'contact_date': timezone.now().strftime("%d-%m-%Y"),
                }

                html_content = render_to_string('main/contact_email.html', context)
                text_content = strip_tags(html_content)

                msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except Exception as e:
                print(f"Contact Email Error: {e}")

            return render(request, "main/contact_us.html", {
                "form": ContactForm(),
                "message": True
            })
        else:
            print("Form Errors:", form.errors)
    else:
        form = ContactForm()

    return render(request, "main/contact_us.html", {"form": form})
def careers(request):
    jobs = Career.objects.filter(status="active").order_by('-posted_date')
    return render(request, "main/career.html", {"jobs": jobs})


def apply_job(request, job_id):
    job = get_object_or_404(Career, id=job_id)

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        current_location = request.POST.get("current_location")
        professional_details = request.POST.get("professional_details")
        total_experience = request.POST.get("total_experience")
        highest_qualification = request.POST.get("highest_qualification")
        notice_period = request.POST.get("notice_period")
        resume = request.FILES.get("resume")

        if not all([full_name, email, phone, current_location, professional_details,
                    total_experience, highest_qualification, resume]):
            return redirect("apply_job", job_id=job_id)

        application = JobApplication.objects.create(
            job=job,
            full_name=full_name,
            email=email,
            phone=phone,
            current_location=current_location,
            professional_details=professional_details,
            total_experience=total_experience,
            highest_qualification=highest_qualification,
            notice_period=notice_period,
            resume=resume
        )

        try:
            subject = 'Application Received - Sakthi Property'
            from_email = 'pavithra.dlktechnologies@gmail.com'
            to_email = [email]

            context = {
                'full_name': full_name,
                'job_title': job.title,
                'applied_on': application.applied_on.strftime("%d-%m-%Y"),
                'application_id': f"SPJ{application.id:04d}",
            }

            html_content = render_to_string('main/job_email.html', context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print(f"Email Error: {e}")

        return redirect("careers")

    return render(request, "main/apply_job.html", {"job": job})