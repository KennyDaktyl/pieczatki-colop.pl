from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# from products.models import Products

# class WorkplaceSiteView(Sitemap):
#     priority = 0.9
#     changefreq = 'daily'
#     protocol = 'https'

#     def items(self):
#         return WorkPlace.objects.all()

# class ProductSiteView(Sitemap):
#     priority = 0.5
#     changefreq = 'weekly'
#     protocol = 'https'

#     def items(self):
#         return Products.objects.filter(is_active=True)

#     def location(self, items):
#         return reverse("product_details_front",
#                        kwargs={
#                            "workplace": items.workplace_id.slug,
#                            "cat": items.sub_category.category.slug,
#                            "sub_cat": items.sub_category.slug,
#                            "slug": items.slug,
#                            "pk": items.id,
#                        })

# class PostSiteView(Sitemap):
#     priority = 0.9
#     changefreq = 'daily'
#     protocol = 'https'

#     def items(self):
#         return Post.objects.filter(blog_article=False)

#     def lastmod(self, obj):
#         return obj.updated

# class PostDetailsSiteView(Sitemap):
#     priority = 0.5
#     changefreq = 'weekly'
#     protocol = 'https'

#     def items(self):
#         return Post.objects.filter(blog_article=False)

#     def location(self, items):
#         return reverse("post_details",
#                        kwargs={
#                            "slug": items.slug,
#                            "pk": items.id,
#                        })

# class BlogsSiteView(Sitemap):
#     priority = 0.9
#     changefreq = 'daily'
#     protocol = 'https'

#     def items(self):
#         return Post.objects.filter(blog_article=True)

#     def lastmod(self, obj):
#         return obj.updated

# class BlogDetailsSiteView(Sitemap):
#     priority = 0.5
#     changefreq = 'weekly'
#     protocol = 'https'

#     def items(self):
#         return Post.objects.filter(blog_article=True)

#     def location(self, items):
#         return reverse("article_details",
#                        kwargs={
#                            "slug": items.slug,
#                            "pk": items.id,
#                        })

# class PromoSiteView(Sitemap):
#     priority = 0.5
#     changefreq = 'weekly'
#     protocol = 'https'

#     def items(self):
#         return Promo.objects.all()

#     def location(self, items):
#         return reverse("promo_details",
#                        kwargs={
#                            "slug": items.slug,
#                            "pk": items.id,
#                        })


class StaticViewSiteMap(Sitemap):
    def items(self):
        return [
            'welcome',
            'products_list',
            'contact_view',
        ]

    def location(self, items):
        return reverse(items)
