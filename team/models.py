from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.models import Orderable, Page

from home.models import NavigationPageMixin


class TeamPage(NavigationPageMixin, Page):
    intro = models.TextField(
        blank=True,
        help_text="A short introduction shown below the page title.",
    )

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        InlinePanel("members", label="Team members", min_num=1),
    ]


class TeamMember(Orderable):
    page = ParentalKey(
        TeamPage,
        on_delete=models.CASCADE,
        related_name="members",
    )
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    bio = models.TextField(blank=True)
    specialties = models.CharField(
        max_length=200,
        blank=True,
        help_text="Optional specialties, separated by commas.",
    )
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    linkedin = models.URLField(blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("photo"),
        FieldPanel("bio"),
        FieldPanel("specialties"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("linkedin"),
    ]

    class Meta:
        ordering = ["sort_order", "name"]
