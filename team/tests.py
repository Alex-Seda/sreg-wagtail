from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from home.models import HomePage
from .models import TeamMember, TeamPage


class TeamPageTests(WagtailPageTestCase):
    def setUp(self):
        self.homepage = HomePage.objects.first()
        if self.homepage is None:
            self.homepage = Page.get_first_root_node().add_child(
                instance=HomePage(title="Home", slug="home")
            )
        self.team_page = self.homepage.add_child(
            instance=TeamPage(title="Our Team", slug="our-team")
        )

    def test_team_page_has_no_child_page_types(self):
        self.assertEqual(self.team_page.allowed_subpage_models(), [])

    def test_team_members_are_ordered_and_renderable(self):
        TeamMember.objects.create(
            page=self.team_page,
            name="Alex Seda",
            role="Broker",
            specialties="Residential sales, relocation",
        )
        TeamMember.objects.create(
            page=self.team_page,
            name="Jordan Lee",
            role="Realtor",
        )

        self.assertEqual(list(self.team_page.members.values_list("name", flat=True)), ["Alex Seda", "Jordan Lee"])
        self.assertPageIsRenderable(self.team_page)
