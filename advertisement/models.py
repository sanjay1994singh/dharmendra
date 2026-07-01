from django.db import models
from django.utils import timezone


class Advertisement(models.Model):
    class Position(models.TextChoices):
        HEADER_TOP = 'header_top', 'Header top'
        HOME_TOP = 'home_top', 'Home top'
        BELOW_HERO = 'below_hero', 'Below hero'
        AFTER_VISUAL_DECK = 'after_visual_deck', 'After visual stories'
        IN_FEED = 'in_feed', 'Inside news feed'
        LATEST_BOTTOM = 'latest_bottom', 'Below latest news'
        CATEGORY_SECTION = 'category_section', 'Between homepage categories'
        CATEGORY_TOP = 'category_top', 'Category top'
        CATEGORY_IN_FEED = 'category_in_feed', 'Inside category feed'
        CATEGORY_BOTTOM = 'category_bottom', 'Category bottom'
        ARTICLE_TOP = 'article_top', 'Article top'
        ARTICLE_AFTER_IMAGE = 'article_after_image', 'Article after image'
        ARTICLE_MIDDLE = 'article_middle', 'Article middle'
        ARTICLE_SIDEBAR = 'article_sidebar', 'Article sidebar'
        ARTICLE_RELATED_BOTTOM = 'article_related_bottom', 'Article related bottom'
        FOOTER_TOP = 'footer_top', 'Footer top'

    class AdType(models.TextChoices):
        IMAGE = 'image', 'Image ad'
        HTML = 'html', 'HTML/script ad'
        TEXT = 'text', 'Text ad'

    title = models.CharField(max_length=160)
    position = models.CharField(max_length=40, choices=Position.choices)
    ad_type = models.CharField(max_length=20, choices=AdType.choices, default=AdType.IMAGE)
    sponsor_name = models.CharField(max_length=120, blank=True)
    image = models.ImageField(upload_to='advertisements', blank=True, null=True)
    target_url = models.URLField(blank=True)
    text = models.CharField(max_length=240, blank=True)
    html_code = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    internal_note = models.CharField(max_length=220, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['position', 'display_order', '-created_at']
        db_table = 'advertisement'

    def __str__(self):
        return f'{self.get_position_display()} - {self.title}'

    @property
    def is_current(self):
        now = timezone.now()
        if not self.is_active:
            return False
        if self.starts_at and self.starts_at > now:
            return False
        if self.ends_at and self.ends_at < now:
            return False
        return True
