from django import template


register = template.Library()


@register.simple_tag
def price_diff(price, limit):
    """
    Returns the difference between the given price and the given limit.
    :param price: the price of the product
    :type price: float
    :param limit: the price limit
    :type limit: float
    :return: formatted string of difference
    :rtype: str
    """
    if price == '':
        return 'No price information available'
    difference = price - limit
    return '%s%.2f' % ('+' if difference >= 0 else '', difference)
