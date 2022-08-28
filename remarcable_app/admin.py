from django.contrib import admin
from remarcable_app.models import Product, Category, Tag, TagProductRelationship, SearchHistory

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(TagProductRelationship)
admin.site.register(SearchHistory)