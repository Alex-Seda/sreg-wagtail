from django.conf import settings
from django.db import models
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.embeds.blocks import EmbedBlock
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail import blocks

from home.blocks import FeaturedTextBlock


BLOG_RICH_TEXT_FEATURES = [
    "h2",
    "h3",
    "h4",
    "bold",
    "italic",
    "link",
    "ol",
    "ul",
]


class BlogHeadingBlock(blocks.CharBlock):
    class Meta:
        template = "blog/blocks/heading.html"


class BlogParagraphBlock(blocks.RichTextBlock):
    class Meta:
        template = "blog/blocks/paragraph.html"


class BlogImageBlock(ImageChooserBlock):
    class Meta:
        template = "blog/blocks/image.html"


class BlogQuoteBlock(blocks.BlockQuoteBlock):
    class Meta:
        template = "blog/blocks/quote.html"


class BlogEmbedBlock(EmbedBlock):
    class Meta:
        template = "blog/blocks/embed.html"


class BlogDocumentBlock(DocumentChooserBlock):
    class Meta:
        template = "blog/blocks/document.html"


class BlogPostBodyBlock(blocks.StreamBlock):
    heading = BlogHeadingBlock(max_length=160, form_classname="title")
    paragraph = BlogParagraphBlock(features=BLOG_RICH_TEXT_FEATURES)
    image = BlogImageBlock()
    quote = BlogQuoteBlock()
    embed = BlogEmbedBlock()
    document = BlogDocumentBlock()
    featured_text = FeaturedTextBlock()


class BlogIndexPage(Page):
    intro = RichTextField(features=BLOG_RICH_TEXT_FEATURES, blank=True)

    parent_page_types = ["home.HomePage", "home.StandardPage"]
    subpage_types = ["blog.BlogPostPage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


class BlogPostPage(Page):
    excerpt = models.TextField(
        blank=True,
        help_text="A short summary used in blog listings and social previews.",
    )
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="blog_posts",
    )
    published_date = models.DateField(
        null=True,
        blank=True,
        help_text="Leave blank to use the page's first published date.",
    )
    body = StreamField(BlogPostBodyBlock(), blank=True)
    tags = ClusterTaggableManager(through="blog.BlogPageTag", blank=True)

    parent_page_types = ["blog.BlogIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("excerpt"),
                FieldPanel("featured_image"),
                FieldPanel("author"),
                FieldPanel("published_date"),
                FieldPanel("tags"),
            ],
            heading="Post details",
        ),
        FieldPanel("body"),
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        BlogPostPage,
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )
