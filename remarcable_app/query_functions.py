from array import array
from remarcable_app.models import Product, Category, Tag, TagProductRelationship

# this function pulls all of the products and their categories from the db and stores them in an array of objects
def pull_all_products() -> array:
    """
        this sql queries the db and performs an inner join with the Product and Category tables where the
        category_id (fk) from the product table and category_id (pk) from the category table match.
    """
    product_table = Product.objects.select_related('category')
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
def pull_all_tags() -> dict:

    """
    this queries the db and performs an inner join with the Poduct table, the Tag table, and the
    TagProductRelationship where each product_id(fk) is matched with its corresponding tag_id(fk)
    """
    tag_table = TagProductRelationship.objects.select_related('product','tag')
    
    tag_data = {}

    """
    take in each row from the new row and parse each coloum to be stored neatly in an array containing
    only the product_name and its corresponding tags.
    """
    for tag in tag_table:
        tags = []

        product_name = str(tag.product)

        """
        since we need to loop through the tag table twice, we need to check if a product has already
        been parsed and stored. We do not want to create duplicate product entries.
        """
        if product_name not in tag_data:
            for tag_match in tag_table:
                if tag.product == tag_match.product:
                    tags.append(str(tag_match.tag))

            tag_data[product_name] = tags

    return tag_data