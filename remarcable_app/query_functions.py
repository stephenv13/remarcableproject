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

def pull_all_categories():
    
    category_data = Category.objects.values_list('category_name', flat=True)
    
    return category_data


def pull_all_tags():

    tag_data = Tag.objects.values_list('tag_name', flat=True)

    return tag_data
