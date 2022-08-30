from django.shortcuts import render
from remarcable_app.models import SearchHistory
from remarcable_app.query_functions import (
    delete_old_searches,
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
    
    """
    we want to pull all of the tables of data we want to use first, so that they can be manipulated by filters.
    
    NOTE: This may not scale well with a large database, however for this case.. It may even be slower to join an entire table,
    then filter in one line of code each time we need specific data VS. pulling everything once and continually
    filtering that down like shown here...
    """
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
     
    """
    we want to pull all of the tables of data we want to use first, so that they can be manipulated by filters.
    """
    
    product_table = pull_all_products()
    tag_product_table = pull_all_tagged_products()
    categories = pull_all_categories()
    just_tags = pull_all_tags()

    search_list = []
    final_products = []

    category_filter = 'None'
    tag_filter = 'None'

    """
    pull the last search term so that if search_results page is refreshed without submitting a new search,
    the search results are still shown and filters can be applied.
    """
    raw_search = str(SearchHistory.objects.last())

    # check if the POST method is from search bar, otherwise it must be from the filters
    if request.method == "POST" and request.POST.get('text_input') is not None:
        
        # pull the raw text from tax string from the search bar
        raw_search = request.POST.get('text_input')

        # create a new search_name object and send it to the database
        latest_search = SearchHistory.objects.create(search_name=raw_search)

        """
        in order to keep the SearchHistory database from getting too large, we will check to see if it is larger
        than 15 entries. If so, call the delete_old_searches function and delete the 10 oldest searches.
        """
        if len(SearchHistory.objects.all().values_list()) > 15:
            delete_old_searches()

        # strip the raw seach string of all white space and store remaining words in an array of strings
        search_list = strip_search_results(raw_search)

        # check to make sure the array is not empty
        if len(search_list) > 0:
            # utilize the search_products function to search entire database and return a list of matching product_ids
            final_products = search_products(search_list,product_table,tag_product_table)

        # filter the displayed product_table based on the matching product_ids found above
        product_table = product_table.filter(id__in = final_products)
    
    else:
        #if no new search is posted.. it must mean filters have been applied

        # strip the raw seach (last search result) string of all white space and store remaining words in an array of strings
        search_list = strip_search_results(raw_search)

        # check to make sure the array is not empty
        if len(search_list) > 0:
            # utilize the search_products function to search entire database and return a list of matching product_ids
            final_products = search_products(search_list,product_table,tag_product_table)

        # filter the displayed product_table based on the matching product_ids found above
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