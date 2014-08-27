class IteratorException(Exception):
    pass


class BaseIterator(object):
    def __init__(
            self, resource_class, resource_uri, params=None, credentials=None):

        self.resource_class = resource_class
        self.resource_uri = resource_uri
        self.params = params
        self.credentials = credentials

        self.index = 0
        self.total_count = None
        self.offset = params.get('offset', 0)
        self.limit = params.get('limit', None)
        self.overall_index = self.offset

        self.objects = self.get_objects()

    def get_total_count(self, content):
        return content['paging']['total_count']

    def process_initial(self, content):
        pass

    def get_objects(self):
        params = self.params or {}
        if self.offset:
            params['offset'] = self.offset
        if self.limit:
            params['limit'] = self.limit

        response = self.resource_class._get(
            self.resource_uri, credentials=self.credentials, params=params)

        if not response.ok:
            raise IteratorException()

        content = response.json()
        if self.total_count is None:
            self.total_count = self.get_total_count(content)
            self.process_initial(content)

        self.prev_offset = self.offset
        self.offset += content['paging']['limit']

        return content['results']

    def __next__(self):
        if not self.objects:
            raise StopIteration()

        if self.index >= self.total_count or self.overall_index >= self.total_count:
            raise StopIteration()

        if len(self.objects) <= self.index:
            self.objects += self.get_objects()

        obj = self.resource_class.build_object_from_dict(
            self.objects[self.index])

        self.index += 1
        self.overall_index += 1

        return obj

    def __iter__(self):
        return self

    # Python 2
    next = __next__


class BaseMercadoLibreIterator(BaseIterator):
    pass


class SearchableIterator(BaseMercadoLibreIterator):
    def get_total_count(self, content):
        return content['paging']['total']

    def process_initial(self, content):
        self.query = content.get('query', None)
        self.seller = content.get('seller', None)
        self.available_filters = content.get('available_filters', None)
