# -*- coding: utf-8 -*-
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel
from wagtail.core.fields import StreamField
from wagtail.core.models import Page, Orderable
from django.db import models
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.snippets.models import register_snippet

from cms_blocks import blocks as cmsblocks


__all__ = (
    'CMSPage',
    'Testimonial'
)


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


class PageTag(TaggedItemBase):
    content_object = ParentalKey('cms.CMSPage', related_name='page_tags')


class AbstractCMSPage(Page):
    """
    Abstract base page for the CMS
    """
    tags = ClusterTaggableManager(through=PageTag, blank=True, help_text='Optional tags used to search for this page')

    content_panels = [
        FieldPanel('title'),
        FieldPanel('tags'),
    ]

    class Meta:
        abstract = True


class CMSPage(AbstractCMSPage):
    parent_page_types = ['wagtailcore.page', 'cms.CMSPage']

    display_title = models.BooleanField(default=True)
    display_banner = models.BooleanField(default=True)

    body = StreamField([
        ('title',           cmsblocks.TitleBlock()),
        ('cards',           cmsblocks.CardsBlock()),
        ('image_and_text',  cmsblocks.ImageAndTextBlock()),
        ('cta',             cmsblocks.CallToActionBlock()),
        ('table',           cmsblocks.CustomTableBlock()),
        ('richtext',        cmsblocks.RichTextWithTitleBlock()),
        ('testimonial',     cmsblocks.TestimonialChooserBlock(help_text='Select testimonial')),
        ('large_image',     cmsblocks.LargeImageChooserBlock(help_text='A large image',)),
        ('new_section',     cmsblocks.NewSectionBlock(help_text='Start a new section')),
    ], blank=True, null=True)

    promote_panels = [
        MultiFieldPanel(
            Page.promote_panels + [
                FieldPanel('display_title'),
                FieldPanel('display_banner')
            ], "Common page configuration"),
    ]

    content_panels = AbstractCMSPage.content_panels + [
        StreamFieldPanel('body')
    ]

    class Meta:
        verbose_name = 'CMS Page'
        verbose_name_plural = 'CMS Pages'


@register_snippet
class Testimonial(models.Model):

    quote = models.TextField(max_length=500, blank=False, null=False)
    attribution = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return f'{self.quote} by {self.attribution}'

    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural= 'Testimonials'
