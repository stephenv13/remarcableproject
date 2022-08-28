from functools import reduce
from django.shortcuts import render
from django.http import HttpResponseRedirect
from remarcable_app.models import Product, Category, Tag, TagProductRelationship, SearchHistory
from remarcable_app.query_functions import (
    pull_all_products,
    pull_all_tagged_products,
    pull_all_categories,
    pull_all_tags,
    products_to_array,
    search_products,
    tags_to_dictionary,
    filter_by_tag,
    filter_by_category,
    strip_search_results
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
    else:
        category_filter = 'None'
        tag_filter = 'None'

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

# this view defines the search results page
def search_results(request):
     
     # we want to pull all of the tables of data we want to use first, so that they can be manipulated by filters
    product_table = pull_all_products()
    tag_product_table = pull_all_tagged_products()
    categories = pull_all_categories()
    just_tags = pull_all_tags()

    search_list = []
    final_products = []

    category_filter = 'None'
    tag_filter = 'None'
    raw_search = str(SearchHistory.objects.last())

    if request.method == "POST" and request.POST.get('text_input') is not None:
        raw_search = request.POST.get('text_input')
        latest_search = SearchHistory.objects.create(search_name=raw_search)

        if raw_search is not None:
            search_list = strip_search_results(raw_search)


        if len(search_list) > 0:
            final_products = search_products(search_list,product_table,tag_product_table)

            
        product_table = product_table.filter(id__in = final_products)
    
    else:

        if raw_search is not None:
            search_list = strip_search_results(raw_search)


        if len(search_list) > 0:
            final_products = search_products(search_list,product_table,tag_product_table)

            
        product_table = product_table.filter(id__in = final_products)

        # pull the currently selected category and tag values from the html radio button
        category_filter = request.POST.get('category')
        tag_filter = request.POST.get('tag')

        # since we have two different filter functions, we must call each one and update the product_table
        product_table = filter_by_category(product_table, category_filter, categories)
        product_table = filter_by_tag(product_table, tag_filter,just_tags)
    

    # utilize helper functions to parse our final sorted/filtered tables into usuable data for the front end
    product_data = products_to_array(product_table)
    tag_data = tags_to_dictionary(tag_product_table)



    return render(request, 'search.html',
    {   
        'product_data': product_data,
        'tag_data':tag_data,
        'raw_search':raw_search,
        'categories':categories,
        'tags':just_tags,
        'category_filter':category_filter,
        'tag_filter': tag_filter
    })