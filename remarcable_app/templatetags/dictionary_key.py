from django.template.defaultfilters import register

# Returns the given key from a dictionary
@register.filter()
def dictionary_key(d, k):
    return d.get(k)