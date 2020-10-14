# -*- coding: utf-8 -*-
from modelcluster.contrib.taggit import ClusterTaggableManager
from modelcluster.fields import ParentalKey
from taggit.models import TaggedItemBase
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, InlinePanel
from wagtail.core.fields import StreamField, RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.images.edit_handlers import ImageChooserPanel
from django.db import models
from taggit.models import Tag as TaggitTag, TaggedItemBase
from wagtail.snippets.models import register_snippet

from cms_blocks import blocks as cmsblocks


__all__ = (
    'CMSPage',
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
        MultiFieldPanel(Page.promote_panels + [FieldPanel('display_title')], "Common page configuration"),
    ]


    content_panels = AbstractCMSPage.content_panels + [
        StreamFieldPanel('body')
    ]

    class Meta:
        verbose_name = 'CMS Page'
        verbose_name_plural = 'CMS Pages'
