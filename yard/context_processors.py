from .models import Inquiry

def unread_inquiries(request):
    if not request.user.is_authenticated:
        return {}
    return {
        'unread_inquiry_count': Inquiry.objects.filter(
            status=Inquiry.Status.NEW
        ).count()
    }
