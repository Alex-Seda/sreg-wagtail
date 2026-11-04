from django.contrib.auth import get_user_model
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from .models import BlogIndexPage, BlogPostPage


class BlogPageTests(WagtailPageTestCase):
    def setUp(self):
        from home.models import HomePage

        self.homepage = HomePage.objects.first()
        if self.homepage is None:
            self.homepage = Page.get_first_root_node().add_child(
                instance=self._home_page()
            )
        self.blog_index = self.homepage.add_child(
            instance=BlogIndexPage(title="Journal", slug="journal")
        )

    def _home_page(self):
        from home.models import HomePage

        return HomePage(title="Home", slug="home")

    def test_blog_post_can_be_created_with_flexible_content(self):
        post = self.blog_index.add_child(
            instance=BlogPostPage(
                title="A thoughtful move",
                slug="a-thoughtful-move",
                excerpt="A short summary.",
                body=[
                    ("heading", "A heading"),
                    ("paragraph", "<p>Formatted content.</p>"),
                    ("quote", "A client quote."),
                ],
            )
        )

        self.assertEqual(post.get_parent().specific, self.blog_index)
        self.assertEqual(len(post.body), 3)
        self.assertEqual(post.body[1].block_type, "paragraph")

    def test_blog_post_supports_author_and_tags(self):
        user = get_user_model().objects.create_user(
            username="writer",
            email="writer@example.com",
        )
        post = self.blog_index.add_child(
            instance=BlogPostPage(title="Market notes", slug="market-notes", author=user)
        )
        post.tags.add("market", "home buying")

        self.assertEqual(post.author, user)
        self.assertCountEqual(post.tags.names(), ["market", "home buying"])
