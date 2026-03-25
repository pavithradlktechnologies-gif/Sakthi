from .models import EmailSetting

def receiver_email_context(request):
    return {
        'receiver_email': EmailSetting.objects.filter(is_selected=True).first(),
        'all_emails': EmailSetting.objects.all().order_by('-id')
    }