from django.db import models
from django.core.exceptions import ValidationError
from django_ckeditor_5.fields import CKEditor5Field


def validate_mp4(value):
    import os
    ext = os.path.splitext(value.name)[1]  # get file extension
    if ext.lower() != '.mp4':
        raise ValidationError("Only .mp4 video files are allowed.")


class Banner_video(models.Model):
    video = models.FileField(upload_to='Banner_videos/', validators=[validate_mp4])
    uploaded_at = models.DateTimeField(auto_now_add=True)


# ---------------------------
# Common Choices
# ---------------------------
PROJECT_TYPE_CHOICES = (
    ('apartment', 'Apartment'),
    ('villa', 'Villa'),
    ('plot', 'Plot'),
    ('form_land', 'Form Land'),
    ('form_house', 'Form House'),
)


# ---------------------------
# Amenities Model (FK)
# ---------------------------
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)  # e.g. "shield-check"

    def __str__(self):
        return self.name


PROJECT_STATUS = (
    ('ongoing','Ongoing'),
    ('completed','Completed'),
    ('up_comming','Up Comming'),
)

# ---------------------------
# Main Project Model
# ---------------------------
class Project(models.Model):
    name = models.CharField(max_length=255)
    project_config = models.CharField(max_length=255)
    project_type = models.CharField(max_length=50, choices=PROJECT_TYPE_CHOICES)
    project_status = models.CharField(max_length=50, choices=PROJECT_STATUS, default='completed')

    price = models.DecimalField(max_digits=12, decimal_places=2)

    # Location fields
    location = models.CharField(max_length=150)  # For filtering
    full_location = models.TextField()
    description = models.TextField() 

    total_units = models.PositiveIntegerField(null=True, blank=True)
    sold_units = models.PositiveIntegerField(null=True, blank=True)

    construction_status = models.PositiveIntegerField(
        help_text="Enter percentage (0–100)",
        null=True,
        blank=True
    )
    # Media
    project_video = models.FileField(upload_to='projects/videos/', blank=True, null=True)
    brochure = models.FileField(upload_to='projects/brochures/', blank=True, null=True)

    # Images (fixed 3)
    image1 = models.ImageField(upload_to='projects/images/')
    image2 = models.ImageField(upload_to='projects/images/')
    image3 = models.ImageField(upload_to='projects/images/')

    # Google Map Embed Link / Coordinates
    google_map_location = models.TextField(help_text="Paste embed iframe or Google Maps link")

    # Amenities (Many-to-Many via FK model)
    amenities = models.ManyToManyField(Amenity, blank=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


# ---------------------------
# Floor Plans (N Images)
# ---------------------------
class FloorPlan(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='floor_plans')
    image = models.ImageField(upload_to='projects/floor_plans/')

    def __str__(self):
        return f"{self.project.name} - Floor Plan"


# ---------------------------
# Gallery (N Images)
# ---------------------------
class Gallery(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='gallery')
    image = models.ImageField(upload_to='projects/gallery/')

    def __str__(self):
        return f"{self.project.name} - Gallery Image"


class LocationCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)  # lucide icon
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

# ---------------------------
# Location Advantages
# ---------------------------
class LocationAdvantage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='location_advantages')

    category = models.ForeignKey(
        LocationCategory,
        on_delete=models.CASCADE,
        related_name='advantages'
    )

    title = models.CharField(max_length=255)
    distance = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.title} - {self.distance}"
    

class BlogPost(models.Model):

    title = models.CharField(max_length=255)
    content = CKEditor5Field('Text')
    image = models.ImageField(upload_to='blog_images/', blank=False, null=True)
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    show_cta = models.BooleanField(default=False)
    cta_text = models.CharField(max_length=100, blank=True)
    cta_link = models.URLField(blank=True)
    comment_show_status = models.BooleanField(default=False)
    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title




class Career(models.Model):
    JOB_TYPE_CHOICES = [
        ("full_time", "Full Time"),
        ("part_time", "Part Time"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
    ]

    title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.CharField(max_length=200)
    experience_required = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    job_summary = models.TextField()
    roles_responsibilities = models.TextField()
    skills_required = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job = models.ForeignKey(Career, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    current_location = models.CharField(max_length=200)
    professional_details = models.TextField()
    total_experience = models.CharField(max_length=50)
    highest_qualification = models.CharField(max_length=200)
    notice_period = models.CharField(max_length=50,null=True,blank=True)
    resume = models.FileField(upload_to="resumes/")

    applied_on = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.full_name} - {self.job.title}"




class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False) 

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
class EmailSetting(models.Model):
    email = models.EmailField(unique=True)
    is_selected = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Project_Enquiry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="enquiries", null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    budget = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.project.name}"