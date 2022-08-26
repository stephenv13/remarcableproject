from django.shortcuts import render
from django.http import HttpResponseRedirect
from remarcable_app.models import Product, Category, Tag, TagProductRelationship
from remarcable_app.query_functions import (
    pull_all_products,
    pull_all_tagged_products,
    pull_all_categories,
    pull_all_tags,
    products_to_array,
    tags_to_dictionary,
    filter_by_tag,
    filter_by_category
)


# this view defines the home landing page
def home(request):
    
    # we want to pull all of the tables of data we want to use first, so that they can be manipulated by filters
    product_table = pull_all_products()
    tag_product_table = pull_all_tagged_products()
    categories = pull_all_categories()
    just_tags = pull_all_tags()
    

    if request.method == "POST":
        # pull the currently selected category and tag values from the html radio button
        category_filter = request.POST.get('category')
        tag_filter = request.POST.get('tag')

        # since we have two different filter functions, we must call each one and update the product_table
        product_table = filter_by_category(product_table, category_filter, categories)
        product_table = filter_by_tag(product_table, tag_filter,just_tags)

    # utilize helper functions to parse our final sorted/filtered tables into usuable data for the front end
    product_data = products_to_array(product_table)
    tag_data = tags_to_dictionary(tag_product_table)


    return render(request,'home.html',
    {
        'product_data': product_data,
        'tag_data':tag_data,
        'categories':categories,
        'tags':just_tags,
        'category_filter':category_filter,
        'tag_filter': tag_filter
    })