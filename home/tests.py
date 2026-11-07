from home.models import HomePage, LegalPage, ServicePage, SiteSettings, StandardPage

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailPageTestCase


class HomeSetUpTests(WagtailPageTestCase):
    """
    Tests for basic page structure setup and HomePage creation.
    """

    def test_root_create(self):
        root_page = Page.objects.get(pk=1)
        self.assertIsNotNone(root_page)

    def test_homepage_create(self):
        root_page = Page.objects.get(pk=1)
        homepage = HomePage(title="Home")
        root_page.add_child(instance=homepage)
        self.assertTrue(HomePage.objects.filter(title="Home").exists())


class HomeTests(WagtailPageTestCase):
    """
    Tests for homepage functionality and rendering.
    """

    def setUp(self):
        """
        Create a homepage instance for testing.
        """
        root_page = Page.get_first_root_node()
        Site.objects.create(hostname="testsite", root_page=root_page, is_default_site=True)
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_homepage_is_renderable(self):
        self.assertPageIsRenderable(self.homepage)

    def test_homepage_template_used(self):
        response = self.client.get(self.homepage.url)
        self.assertTemplateUsed(response, "home/home_page.html")


class ContentPageTests(WagtailPageTestCase):
    def setUp(self):
        root_page = Page.get_first_root_node()
        self.site = Site.objects.create(
            hostname="testsite", root_page=root_page, is_default_site=True
        )
        self.homepage = HomePage(title="Home")
        root_page.add_child(instance=self.homepage)

    def test_standard_page_can_be_created_under_homepage(self):
        page = StandardPage(title="About Us")
        self.homepage.add_child(instance=page)

        self.assertPageIsRenderable(page)
        self.assertTemplateUsed(self.client.get(page.url), "home/standard_page.html")

    def test_service_page_can_be_created_under_homepage(self):
        page = ServicePage(title="Move Coordination")
        self.homepage.add_child(instance=page)

        self.assertPageIsRenderable(page)
        self.assertTemplateUsed(self.client.get(page.url), "home/service_page.html")

    def test_service_page_cannot_have_children(self):
        page = ServicePage(title="Move Coordination")
        self.homepage.add_child(instance=page)

        self.assertEqual(page.allowed_subpage_models(), [])

    def test_legal_page_can_be_created_under_homepage(self):
        page = LegalPage(title="Privacy Policy")
        self.homepage.add_child(instance=page)

        self.assertPageIsRenderable(page)
        self.assertTemplateUsed(self.client.get(page.url), "home/legal_page.html")

    def test_configured_legal_pages_are_shown_in_footer(self):
        page = LegalPage(title="Privacy Policy")
        self.homepage.add_child(instance=page)
        SiteSettings.objects.create(site=self.site, privacy_policy=page)

        response = self.client.get(self.homepage.url)

        self.assertContains(response, f'href="{page.url}"')
        self.assertContains(response, "Privacy Policy")
        self.assertNotContains(response, "Terms of Use")
