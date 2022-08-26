from array import array
from remarcable_app.models import Product, Category, Tag, TagProductRelationship

# this function pulls all of the products and their categories from the db
def pull_all_products():
    """
        this sql queries the db and performs an inner join with the Product and Category tables where the
        category_id (fk) from the product table and category_id (pk) from the category table match.
    """
    product_table = Product.objects.select_related('category')
    
    return product_table

# this function takes in an entire table of products and stores them in an array of objects
def products_to_array(product_table):
    data = []

    # take in each row from the new table and parse each column to be stored in the data array
    for product in product_table:
        entry = product.id
        product_name = product.product_name
        category = product.category

        data.append({
            'entry': entry,
            'product_name': product_name,
            'category': category
        })
    return data

# this function pulls all of the product names and their correspondig tags from the db and stores them in a dictionary.
def pull_all_tagged_products() -> dict:

    """
    this queries the db and performs an inner join with the Poduct table, the Tag table, and the
    TagProductRelationship where each product_id(fk) is matched with its corresponding tag_id(fk)
    """
    tag_table = TagProductRelationship.objects.select_related('product','tag')

    return tag_table
    
    
# this fucntion takes in an entire table of products and their corresponding tags and parses them to a dictionary
def tags_to_dictionary(tag_product_table):
    tag_data = {}

    """
    take in each row from the new row and parse each coloum to be stored neatly in an array containing
    only the product_name and its corresponding tags.
    """
    for tag in tag_product_table:
        tags = []

        product_name = str(tag.product)

        """
        since we need to loop through the tag table twice, we need to check if a product has already
        been parsed and stored. We do not want to create duplicate product entries.
        """
        if product_name not in tag_data:
            for tag_match in tag_product_table:
                if tag.product == tag_match.product:
                    tags.append(str(tag_match.tag))

            tag_data[product_name] = tags

    return tag_data

"""
NEEDS COMMENT
"""
def pull_all_categories():
    
    category_data = Category.objects.values_list('category_name', flat=True)
    
    return category_data

"""
NEEDS COMMENT
"""
def pull_all_tags():

    tag_data = Tag.objects.values_list('tag_name', flat=True)

    return tag_data

"""
this function takes in the product_table, the currently selected tag_filter, and the table of tags. It filters
the product table based on the selected tag filter and returns the updated product_table
"""
def filter_by_tag(product_table, tag_filter, just_tags):
    # check to see if the selected filter is a tag
    if tag_filter in just_tags:
        """
        In order to filter our products by tags and display them correctly:

        1. find all product_ids that use the selected tag filter
        2. filter the product_table to contain only the product_ids found in step 1
        """

        """
        this query selects the matching Tag object from the Tag table with the applied filter name. This is
        assigned to a variable that we can manipulate to grab its corresponding id
        """
        tag_name = Tag.objects.get(tag_name = tag_filter)

        """
        this queries the TagProductRelationship and filters it to only contain products that match our selected
        filter and its corresponding tag_id.
        """
        selected_products = TagProductRelationship.objects.filter(tag_id = tag_name.id)

        # pull all product_ids from the new table of selected_products and store them in an array
        products = []
        for product in selected_products:
            products.append(product.product_id)

        """
        this query filters the product table based on our array of product_ids
        """
        product_table = product_table.filter(id__in = products)
    
    return product_table

"""
this function takes in the product_table, the currently selected category_filter, and the table of categories. It filters
the product table based on the selected category filter and returns the updated product_table
"""
def filter_by_category(product_table, category_filter, categories):
    # check to see if the selected filter is a category
    if category_filter in categories:
        """
        this query selects the matching Category object with the applied filter name. This is assigned to 
        a variable that we can manipulate to grab its corresponding id
        """
        category_name = Category.objects.get(category_name = category_filter)

        """
        this query filters the product_table we created earlier and filters it to contain products
        that match the category_id of the selected category filter.
        """
        product_table = product_table.filter(category_id = category_name.id)
    
    return product_table
