from django.db import models

"""
This model class will produce a table containing a pk column, product_name column, and a category fk column. The fk links each
product with its corresponding category.
"""
class Product(models.Model):
    product_name = models.CharField(max_length=20)
    category = models.ForeignKey('remarcable_app.category', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.product_name


"""
This model class will produce a table containing a pk column and a category_name column.
"""
class Category(models.Model):
    category_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.category_name


"""
This model class will produce a table containing a pk column and a tag_name column.
"""
class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.tag_name

"""
This model class will produce a table containing a pk column and two fk columns. These fk columns link each product with
its corresponding tags.
"""
class TagProductRelationship(models.Model):
    product = models.ForeignKey("remarcable_app.product",on_delete=models.CASCADE)
    tag = models.ForeignKey("remarcable_app.tag",on_delete=models.CASCADE)

"""
This model class will produce a table containing a pk column and a search_name column. It will store 
a string of each latest search from the search bar.
"""
class SearchHistory(models.Model):
    search_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.search_name