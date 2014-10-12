import hashlib
import math
import pygal

from ... import app_settings

from django.core.cache import get_cache
from rest_framework.renderers import BaseRenderer

from tempfile import TemporaryFile


class PriceChartPNGRenderer(BaseRenderer):
    """
    A renderer to render charts as PNG for prices
    """

    media_type = 'image/*'
    format = 'png'
    charset = None
    render_style = 'binary'
    
    # TODO: documentation
    allowed_url_args = {
        'height': lambda x: int(x),
        'width': lambda x: int(x),
    }

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        # first get the cache to use or None
        cache = get_cache(app_settings.PRICE_MONITOR_GRAPH_CACHE_NAME) if app_settings.PRICE_MONITOR_GRAPH_CACHE_NAME is not None else None
        # generate cache key
        cache_key = self.create_cache_key(
            data, 
            self.sanitize_allowed_args(renderer_context['request']) if 'request' in renderer_context else None
        )
        # only read from cache if there is any
        content = cache.get(cache_key, None) if cache is not None else None
        if content is None:
            # create graph instance
            graph = self.create_graph(data)

            # write graph to temporary file
            with TemporaryFile() as file_:
                graph.render_to_png(file_)

                # only write to cache if there is any
                if cache is not None:
                    # seek back to start
                    file_.seek(0)
                    cache.set(cache_key, file_.read())
                # and back to start again
                file_.seek(0)
                # return the content
                return file_.read()
        else:
            # return the cache content
            return content
        
    def sanitize_allowed_args(self, request):
        """
        TODO: documentation
        """
        sanitized_args = {}
        if request.method == 'POST':
            args = request.POST
        elif request.method == 'GET':
            args = request.GET
        else:
            return sanitized_args
        
        for arg, sanitizer in self.allowed_url_args.iteritems():
            if arg in args:
                try:
                    sanitized_args[arg] = sanitizer(args[arg])
                except ValueError:
                    # sanitation gone wrong, so pass
                    pass
        return sanitized_args

    def create_cache_key(self, data, args=None):
        """
        Creates a cache key based on rendering data
        """
        hash_data = unicode(data['results'])
        if args is not None:
            hash_data += unicode(args)
        return app_settings.PRICE_MONITOR_GRAPH_CACHE_KEY_PREFIX + hashlib.md5(hash_data).hexdigest()

    def create_graph(self, data):
        """
        Creates the graph based on rendering data
        """
        line_chart = pygal.Line(
            show_minor_y_labels=False,
            y_labels_major_count=5,
        )
        values = []
        if 'results' in data and len(data['results']) > 0:
            values = [price['value'] for price in data['results']]
            #line_chart.x_labels = [price['date_seen'] for price in data['results']]
            #line_chart.y_labels = range(int(math.floor(min(values)))-1, int(math.ceil(max(values))) + 1)
            #print line_chart.y_labels
        line_chart.add(data['results'][0]['currency'], values)
        return line_chart