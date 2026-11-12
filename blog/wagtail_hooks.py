from django.urls import reverse
from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.models import Site

from .models import BlogIndexPage


class BlogMenuItem(MenuItem):
    def get_blog_index(self, request):
        site = Site.find_for_request(request)
        if site is None:
            return None
        return (
            site.root_page
            .get_descendants()
            .type(BlogIndexPage)
            .live()
            .first()
        )

    def is_shown(self, request):
        return self.get_blog_index(request) is not None

    def render_component(self, request):
        blog_index = self.get_blog_index(request)
        if blog_index is not None:
            self.url = reverse("wagtailadmin_explore", args=[blog_index.id])
        return super().render_component(request)


@hooks.register("register_admin_menu_item")
def register_blog_menu_item():
    return BlogMenuItem(
        "Blog",
        "#",
        name="blog",
        icon_name="doc-full-inverse",
        order=200,
    )
