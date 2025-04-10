from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)
    
    # Include only published posts, in reverse chronological order
    def get_context(self, request):
        context = super().get_context(request)
        blogpages = self.get_children().live().order_by('-first_published_at')
        context['blogpages'] = blogpages
        return context
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
    
class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )
    
class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank = True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    
    #Add the main_image method:
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None
    
    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]
    
    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading="Blog information"),
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        # Make gallery images available on blogpost editing interface:
        InlinePanel('gallery_images', label="Gallery images"),
    ]

# Inheriting from Orderable adds a sort_order field to the model to keep track of the ordering of images in the gallery.  
class BlogPageGalleryImage(Orderable):
    # ParentalKey attaches gallery images to a specific page, defines this class as a child of BlogPage class.
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images') 
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    
    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
    
@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
        
    panels = [
        FieldPanel('name'),
        FieldPanel('author_image'),
    ]
        
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Authors'
        
class BlogTagIndexPage(Page):
    def get_context(self, request):
        #Filter by tag
        tag = request.GET.get('tag')
        blogpages=BlogPage.objects.filter(tags__name=tag)
        
        context = super().get_context(request)
        context['blogpages'] = blogpages
        return context
