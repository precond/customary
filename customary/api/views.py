from customary.api import api_request


@api_request(methods=['GET', 'POST'])
def status(request, data):
    """
    A status view for querying the API availability with given token.
    Can be used e.g. by monitoring systems to poll the service. Note
    that the @api_request has hit the database to look up the token,
    so this view will monitor database availability as well.
    """
    return dict()
