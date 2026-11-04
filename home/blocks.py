from wagtail import blocks
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock

RICH_FEATURES = ["bold", "italic", "link", "ul", "ol"]
INLINE_FEATURES = ["bold", "italic", "link"]


def background_choice():
    return blocks.ChoiceBlock(
        choices=[("linen", "Light"), ("sand", "Sand")],
        default="linen",
        help_text="Alternate backgrounds between neighbouring sections.",
    )


class LinkBlock(blocks.StructBlock):
    """A button. Leave the label empty and the button is not rendered."""

    label = blocks.CharBlock(required=False, max_length=40, help_text="Leave blank to hide the button.")
    page = blocks.PageChooserBlock(required=False)
    url = blocks.CharBlock(
        required=False,
        help_text="Used when no page is chosen. Accepts https://, tel: and mailto: links.",
    )

    class Meta:
        icon = "link"
        label = "Button"


# --- Hero -------------------------------------------------------------------

class HeroBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    subheading = blocks.TextBlock(required=False, max_length=300)
    image = ImageChooserBlock()
    primary_cta = LinkBlock(required=False, label="Primary button")
    secondary_cta = LinkBlock(required=False, label="Secondary button")
    text_position = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("center", "Centered")], default="left"
    )

    class Meta:
        template = "blocks/hero_block.html"
        icon = "image"
        label = "Hero"


class SecondaryHeroBlock(blocks.StructBlock):
    eyebrow = blocks.CharBlock(max_length=60, required=False)
    heading = blocks.CharBlock(max_length=120)
    subheading = blocks.TextBlock(required=False, max_length=300)
    image = ImageChooserBlock()
    cta = LinkBlock(required=False, label="Button")
    image_side = blocks.ChoiceBlock(
        choices=[("right", "Image on right"), ("left", "Image on left")],
        default="right",
    )

    class Meta:
        template = "blocks/secondary_hero_block.html"
        icon = "image"
        label = "Secondary hero"


# --- Statement (big serif paragraph) -----------------------------------------

class StatementBlock(blocks.StructBlock):
    body = blocks.RichTextBlock(features=INLINE_FEATURES, help_text="One or two sentences works best.")
    link = LinkBlock(required=False, label="Button")
    background = background_choice()

    class Meta:
        template = "blocks/statement_block.html"
        icon = "openquote"
        label = "Statement"


# --- Image + text ------------------------------------------------------------

class ImageTextBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    heading = blocks.CharBlock(max_length=120)
    body = blocks.RichTextBlock(features=RICH_FEATURES)
    link = LinkBlock(required=False, label="Button")
    image_side = blocks.ChoiceBlock(
        choices=[("left", "Left"), ("right", "Right")], default="left"
    )
    background = background_choice()

    class Meta:
        template = "blocks/image_text_block.html"
        icon = "doc-full"
        label = "Image and text"


# --- Listings ----------------------------------------------------------------

class ListingBlock(blocks.StructBlock):
    image = ImageChooserBlock()
    status = blocks.ChoiceBlock(
        required=False,
        choices=[
            ("Just listed", "Just listed"),
            ("Under contract", "Under contract"),
            ("Sold", "Sold"),
        ],
    )
    address = blocks.CharBlock(max_length=120)
    city = blocks.CharBlock(max_length=80, required=False, help_text="e.g. Stillwater, OK")
    price = blocks.CharBlock(max_length=30, help_text="Typed as you want it shown, e.g. $425,000")
    beds = blocks.IntegerBlock(required=False, min_value=0)
    baths = blocks.DecimalBlock(required=False, max_digits=3, decimal_places=1, min_value=0)
    sqft = blocks.IntegerBlock(required=False, min_value=0, label="Square feet")
    page = blocks.PageChooserBlock(required=False, label="Details page")
    url = blocks.URLBlock(required=False, label="Or external link")

    class Meta:
        icon = "home"
        label_format = "{address}"


class ListingsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, required=False)
    intro = blocks.TextBlock(required=False, max_length=300)
    listings = blocks.ListBlock(ListingBlock(), min_num=1, max_num=12)
    view_all = LinkBlock(required=False, label="View all button")
    background = background_choice()

    class Meta:
        template = "blocks/listings_block.html"
        icon = "home"
        label = "Featured listings"


# --- Services ----------------------------------------------------------------

class ServiceItemBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=80)
    description = blocks.TextBlock(max_length=400)
    link = LinkBlock(required=False, label="Link")

    class Meta:
        icon = "list-ul"
        label_format = "{title}"


class ServicesBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    intro = blocks.TextBlock(required=False, max_length=300)
    items = blocks.ListBlock(ServiceItemBlock(), min_num=1, max_num=8)
    background = background_choice()

    class Meta:
        template = "blocks/services_block.html"
        icon = "list-ul"
        label = "Services"


# --- Team --------------------------------------------------------------------

class PersonBlock(blocks.StructBlock):
    photo = ImageChooserBlock()
    name = blocks.CharBlock(max_length=80)
    role = blocks.CharBlock(max_length=80, required=False)
    bio = blocks.TextBlock(required=False, max_length=500)
    phone = blocks.CharBlock(max_length=30, required=False)
    email = blocks.EmailBlock(required=False)

    class Meta:
        icon = "user"
        label_format = "{name}"


class TeamBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    intro = blocks.TextBlock(required=False, max_length=300)
    people = blocks.ListBlock(PersonBlock(), min_num=1, max_num=12)
    background = background_choice()

    class Meta:
        template = "blocks/team_block.html"
        icon = "group"
        label = "Team"


# --- Testimonials ------------------------------------------------------------

class TestimonialItemBlock(blocks.StructBlock):
    quote = blocks.TextBlock(max_length=500)
    name = blocks.CharBlock(max_length=80)
    detail = blocks.CharBlock(max_length=100, required=False, help_text="e.g. Sold in Stillwater, 2025")

    class Meta:
        icon = "openquote"
        label_format = "{name}"


class TestimonialsBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, required=False)
    items = blocks.ListBlock(TestimonialItemBlock(), min_num=1, max_num=6)
    background = background_choice()

    class Meta:
        template = "blocks/testimonials_block.html"
        icon = "openquote"
        label = "Testimonials"


# --- FAQ ---------------------------------------------------------------------

class FAQItemBlock(blocks.StructBlock):
    question = blocks.CharBlock(max_length=200)
    answer = blocks.RichTextBlock(features=RICH_FEATURES)

    class Meta:
        icon = "help"
        label_format = "{question}"


class FAQBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    items = blocks.ListBlock(FAQItemBlock(), min_num=1)
    background = background_choice()

    class Meta:
        template = "blocks/faq_block.html"
        icon = "help"
        label = "FAQ"


# --- Video / embed -----------------------------------------------------------

class VideoBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, required=False)
    embed = EmbedBlock(help_text="YouTube or Vimeo link.")

    class Meta:
        template = "blocks/video_block.html"
        icon = "media"
        label = "Video"


# --- Plain rich text ---------------------------------------------------------

class RichTextSectionBlock(blocks.RichTextBlock):
    def __init__(self, **kwargs):
        kwargs.setdefault("features", ["h2", "h3", *RICH_FEATURES])
        super().__init__(**kwargs)

    class Meta:
        template = "blocks/rich_text_block.html"
        icon = "doc-full"
        label = "Text"


# --- Featured text -----------------------------------------------------------

class FeaturedTextBlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120, required=False)
    body = blocks.RichTextBlock(features=RICH_FEATURES)
    level = blocks.ChoiceBlock(
        choices=[
            ("strong", "Strong contrast"),
            ("medium", "Featured"),
            ("subtle", "Subtle"),
        ],
        default="strong",
        help_text="Use Strong contrast for the most prominent callout.",
    )
    background = blocks.ChoiceBlock(
        choices=[
            ("dark", "Dark umber"),
            ("sand", "Sand"),
            ("light", "Light linen"),
        ],
        default="dark",
    )

    class Meta:
        template = "blocks/featured_text_block.html"
        icon = "warning"
        label = "Featured text"


# --- Call to action ----------------------------------------------------------

class CTABlock(blocks.StructBlock):
    heading = blocks.CharBlock(max_length=120)
    text = blocks.TextBlock(required=False, max_length=300)
    primary_cta = LinkBlock(required=False, label="Primary button")
    secondary_cta = LinkBlock(required=False, label="Secondary button")
    style = blocks.ChoiceBlock(
        choices=[("dark", "Dark"), ("sand", "Sand")], default="dark"
    )

    class Meta:
        template = "blocks/cta_block.html"
        icon = "mail"
        label = "Call to action"


# --- The StreamField ---------------------------------------------------------

class HomeStreamBlock(blocks.StreamBlock):
    hero = HeroBlock()
    secondary_hero = SecondaryHeroBlock()
    statement = StatementBlock()
    image_text = ImageTextBlock()
    listings = ListingsBlock()
    services = ServicesBlock()
    team = TeamBlock()
    testimonials = TestimonialsBlock()
    faq = FAQBlock()
    video = VideoBlock()
    rich_text = RichTextSectionBlock()
    featured_text = FeaturedTextBlock()
    cta = CTABlock()

    class Meta:
        block_counts = {"hero": {"max_num": 1}}


class StandardStreamBlock(blocks.StreamBlock):
    hero = HeroBlock()
    secondary_hero = SecondaryHeroBlock()
    statement = StatementBlock()
    image_text = ImageTextBlock()
    testimonials = TestimonialsBlock()
    faq = FAQBlock()
    video = VideoBlock()
    rich_text = RichTextSectionBlock()
    featured_text = FeaturedTextBlock()
    cta = CTABlock()


class ServiceStreamBlock(blocks.StreamBlock):
    hero = HeroBlock()
    secondary_hero = SecondaryHeroBlock()
    statement = StatementBlock()
    image_text = ImageTextBlock()
    services = ServicesBlock()
    testimonials = TestimonialsBlock()
    faq = FAQBlock()
    video = VideoBlock()
    rich_text = RichTextSectionBlock()
    featured_text = FeaturedTextBlock()
    cta = CTABlock()

    class Meta:
        block_counts = {"hero": {"max_num": 1}}
