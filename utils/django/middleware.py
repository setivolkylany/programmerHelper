
import time

from django.db import connection
from django.utils import timezone


class LastSeenAccountMiddleware(object):
    """
    Middleware for trace down time last seen on website.
    """

    def process_response(self, request, response):
        if request.user.is_authenticated() and response.status_code == 200:
            request.session['last_seen'] = timezone.now()
        return response


class TimeLoadPageMiddleware(object):
    """
    Middleware for tracing time load of page.
    """

    def process_request(self, request):
        """Method calling after request page."""

        # keep a time on start load a page
        self.time_on_start_load_page = time.time()

    def process_response(self, request, response):
        """Method calling after page is loaded."""

        # determinate duration load of page
        # as different between time on start load tha page and on after page is loaded

        # in seconds
        duration = time.time() - self.time_on_start_load_page

        # in microseconds
        duration = duration * 1000

        # Add the header
        response["X-Page-Generation-Duration-ms"] = duration

        return response


class CountQueriesMiddleware(object):
    """
    Middleware for tracing count queries for a database after page is loaded.
    """

    def process_request(self, request):
        """Method calling after request page."""

        # set count request to 0
        self.count_request = 0

    def process_response(self, request, response):
        """Method calling after page is loaded."""

        # determinate duration load of page
        # as different between time on start load tha page and on after page is loaded
        count_queries = len(connection.queries)
        # in mkseconds
        time_excecution_all_queries = sum(float(query.get('time'),) for query in connection.queries) * 1000
        a = list()
        for i, query in enumerate(connection.queries):
            a.append((i, query.get('time')))
        # Add the header.
        # response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        return response