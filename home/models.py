from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import HomeStreamBlock, ServiceStreamBlock, StandardStreamBlock


class HomePage(Page):
    body = StreamField(HomeStreamBlock(), blank=True)

    max_count = 1
    parent_page_types = ["wagtailcore.Page"]
    subpage_types = [
        "home.StandardPage",
        "home.ServicePage",
        "blog.BlogIndexPage",
        "team.TeamPage",
    ]

    content_panels = Page.content_panels + [FieldPanel("body")]


class StandardPage(Page):
    body = StreamField(StandardStreamBlock(), blank=True)

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = [
        "home.StandardPage",
        "home.ServicePage",
        "blog.BlogIndexPage",
        "team.TeamPage",
    ]

    content_panels = Page.content_panels + [FieldPanel("body")]


class ServicePage(Page):
    body = StreamField(ServiceStreamBlock(), blank=True)

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = []

    content_panels = Page.content_panels + [FieldPanel("body")]


@register_setting(icon="cog")
class SiteSettings(BaseSiteSetting):
    """Header/footer details, editable under Settings in the admin."""

    business_name = models.CharField(max_length=100, default="Seda Real Estate Group")
    site_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Shown in the site header. Falls back to the business name when blank.",
    )
    team_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional team or company logo shown in the footer.",
    )
    broker_logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Optional brokerage logo shown in the footer.",
    )
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    license_info = models.TextField(
        blank=True,
        help_text="Shown in the footer, e.g. brokerage license and Equal Housing Opportunity statement.",
    )
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
