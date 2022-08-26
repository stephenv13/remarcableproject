from django.shortcuts import render
from remarcable_app.models import Product, Category, Tag, TagProductRelationship
from remarcable_app.query_functions import pull_all_products, pull_all_tags

# this view defines the home landing page
def home(request):
    
    # utilize query functions from query_functions.py
    data = pull_all_products()
    tag_data = pull_all_tags()
    
    return render(request,'home.html',{'data': data,'tag':tag_data})