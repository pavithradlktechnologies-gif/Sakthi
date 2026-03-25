from django.shortcuts import render, redirect, get_object_or_404
from admin_dashboard.models import *
from collections import defaultdict
from .forms import *
from django.http import JsonResponse

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

            return render(request, "main/contact_us.html", {
                "form": ContactForm(),
                "message": True
            })
        else:
            print("=============", form.errors)
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

        # Basic validation
        if not all([full_name, email, phone, current_location, professional_details,
                    total_experience, highest_qualification, resume]):
            return redirect("apply_job", job_id=job_id)

        # Save form
        JobApplication.objects.create(
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

        return redirect("careers")

    return render(request, "main/apply_job.html", {"job": job})