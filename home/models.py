from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.fields import StreamField
from wagtail.models import ClusterableModel, Orderable, Page

from .blocks import HomeStreamBlock, ServiceStreamBlock, StandardStreamBlock


class NavigationPageMixin:
    def get_navigation_children(self):
        return self.get_children().live().in_menu()


class HomePage(NavigationPageMixin, Page):
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


class StandardPage(NavigationPageMixin, Page):
    body = StreamField(StandardStreamBlock(), blank=True)

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = [
        "home.StandardPage",
        "home.ServicePage",
        "blog.BlogIndexPage",
        "team.TeamPage",
    ]

    content_panels = Page.content_panels + [FieldPanel("body")]


class ServicePage(NavigationPageMixin, Page):
    body = StreamField(ServiceStreamBlock(), blank=True)

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = []

    content_panels = Page.content_panels + [FieldPanel("body")]


@register_setting(icon="cog")
class SiteSettings(BaseSiteSetting, ClusterableModel):
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

    panels = [
        FieldPanel("business_name"),
        FieldPanel("site_logo"),
        FieldPanel("team_logo"),
        FieldPanel("broker_logo"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("address"),
        FieldPanel("license_info"),
        FieldPanel("facebook"),
        FieldPanel("instagram"),
        FieldPanel("linkedin"),
        FieldPanel("tiktok"),
        FieldPanel("youtube"),
        InlinePanel(
            "main_navigation_items",
            label="Custom main navigation",
            help_text="Choose the top-level pages to show. Their live child pages will appear as submenus.",
        ),
    ]

    def get_main_navigation_items(self):
        return (
            self.main_navigation_items.filter(
                models.Q(page__isnull=True) | models.Q(page__live=True)
            )
            .prefetch_related("submenu_items__page")
            .select_related("page")
        )


class MainNavigationItem(Orderable, ClusterableModel):
    settings = ParentalKey(
        SiteSettings,
        on_delete=models.CASCADE,
        related_name="main_navigation_items",
    )
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional label. Defaults to the selected page title.",
    )
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        limit_choices_to={"live": True},
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("page"),
        InlinePanel("submenu_items", label="Submenu items"),
    ]

    def get_label(self):
        return self.label or (self.page.title if self.page else "")


class MainNavigationSubItem(Orderable):
    navigation_item = ParentalKey(
        MainNavigationItem,
        on_delete=models.CASCADE,
        related_name="submenu_items",
    )
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional label. Defaults to the selected page title.",
    )
    page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="+",
        limit_choices_to={"live": True},
    )

    panels = [
        FieldPanel("label"),
        FieldPanel("page"),
    ]

    def get_label(self):
        return self.label or (self.page.title if self.page else "")
