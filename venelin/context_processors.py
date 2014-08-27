from django.conf import settings


def google_analytics(request):
    if settings.DEBUG or request.user.is_staff:
        return {}
    return {
        'GOOGLE_ANALYTICS_CODE': getattr(settings, 'GOOGLE_ANALYTICS_CODE', None),
        'GOOGLE_ANALYTICS_DOMAIN': getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', request.get_host()),
    }
