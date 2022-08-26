from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from remarcable_app.models import Product, Category, Tag, TagProductRelationship
from remarcable_app.query_functions import (
    pull_all_products,
    pull_all_tagged_products,
    pull_all_categories,
    pull_all_tags,
    products_to_array,
    tags_to_dictionary
)


# this view defines the home landing page
def home(request):
    
    # utilize query functions from query_functions.py
    product_table = pull_all_products()
    tag_product_table = pull_all_tagged_products()
    categories = pull_all_categories()
    just_tags = pull_all_tags()
    
    cur_filter = 'No Filters Applied'

    if request.method == "POST":
        category_filter = request.POST.get('category')
        tag_filter = request.POST.get('tag')


        # check to see if the selected filter is a category
        if category_filter in categories:
            category_name = Category.objects.get(category_name = category_filter)
            product_table = product_table.filter(category_id = category_name.id)
            cur_filter = category_filter

        # check to see if the selected filter is a tag
        if tag_filter in just_tags:
            """
            In order to filter our products by tags and display them correctly:

            1. find all product_ids that use the selected tag filter
            2. filter the product_table to contain only the product_ids found in step 1
            """

            tag_name = Tag.objects.get(tag_name = tag_filter)
            selected_products = TagProductRelationship.objects.filter(tag_id = tag_name.id)

            products = []
            for product in selected_products:
                products.append(product.product_id)

            product_table = product_table.filter(id__in = products)

    

    product_data = products_to_array(product_table)
    tag_data = tags_to_dictionary(tag_product_table)

    

    return render(request,'home.html',
    {
        'product_data': product_data,
        'tag_data':tag_data,
        'categories':categories,
        'tags':just_tags,
        'str':cur_filter,
    })