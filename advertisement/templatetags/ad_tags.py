from django import template
from django.utils import timezone

from advertisement.models import Advertisement

register = template.Library()


@register.inclusion_tag('partials/ad_slot.html', takes_context=True)
def render_ad(context, position):
    now = timezone.now()
    ad = (
        Advertisement.objects
        .filter(is_active=True, position=position)
        .filter(models_start_filter(now))
        .filter(models_end_filter(now))
        .order_by('display_order', '-created_at')
        .first()
    )

    return {
        'ad': ad,
        'position': position,
        'request': context.get('request'),
    }


def models_start_filter(now):
    from django.db.models import Q
    return Q(starts_at__isnull=True) | Q(starts_at__lte=now)


def models_end_filter(now):
    from django.db.models import Q
    return Q(ends_at__isnull=True) | Q(ends_at__gte=now)
