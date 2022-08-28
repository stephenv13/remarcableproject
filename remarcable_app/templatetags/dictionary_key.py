from django.template.defaultfilters import register

# Returns the given key from a dictionary
@register.filter()
def dictionary_key(d, k):
    # we use d.get(k) so that an error is not thrown if there is nothing in the dictionary. It just returns None
    return d.get(k)