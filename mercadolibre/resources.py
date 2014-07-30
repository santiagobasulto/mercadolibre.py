import json

from . import http
from . import config
from mercadolibre.exceptions import MercadoLibreException

__all__ = [
    'ItemResource', 'MLASiteResource', 'UserResource', 'CategoryResource',
    'ItemDescriptionResource', 'TestUser']


class BaseResource(object):
    LIST_RESOURCE_ENDPOINT = "{root}/{resource_name}/"

    # Needs to be overridden by subclass Resources
    RESOURCE_NAME = None

    @classmethod
    def get_collection_resource_endpoint(cls, sub_resource=None):
        if not hasattr(cls, 'RESOURCE_NAME'):
            raise ValueError(
                "The resource didn't specify a RESOURCE_NAME variable")

        url = cls.LIST_RESOURCE_ENDPOINT.format(
            root=config.API_ROOT,
            resource_name=cls.RESOURCE_NAME
        )
        if sub_resource:
            url += sub_resource

        return url

    @classmethod
    def get_detail_resource_endpoint(cls, id):
        if not hasattr(cls, 'RESOURCE_NAME'):
            raise ValueError(
                "The resource didn't specify a RESOURCE_NAME variable")

        list_endpoint = cls.LIST_RESOURCE_ENDPOINT.format(
            root=config.API_ROOT,
            resource_name=cls.RESOURCE_NAME
        )
        return list_endpoint + "{id}/".format(id=id)

    @classmethod
    def get(cls, id=None, params=None, credentials=None):
        if id:
            return cls.get_detail(id, params=params, credentials=credentials)
        else:
            return cls.get_collection(params=params, credentials=credentials)

    @classmethod
    def get_iterator_for_collection(cls):
        from .iterators import BaseMercadoLibreIterator
        return BaseMercadoLibreIterator

    @classmethod
    def build_object_from_dict(cls, data_dict, credentials=None):
        kwargs = {
            'data': data_dict,
            'credentials': credentials
        }
        obj = cls(**kwargs)
        obj._data = data_dict
        return obj

    @classmethod
    def _request(cls, method, url, session=None, credentials=None, **kwargs):
        credentials = cls.get_credentials(credentials=credentials)
        session = session or cls.get_session(credentials=credentials)
        response = session.request(method, url, **kwargs)
        return response

    _get = classmethod(
        lambda cls, url, **kwargs: cls._request('GET', url, **kwargs))

    _post = classmethod(
        lambda cls, url, **kwargs: cls._request('POST', url, **kwargs))

    @classmethod
    def post(cls, data=None, params=None, credentials=None):
        resource_url = cls.get_collection_resource_endpoint()
        kwargs = {
            'url': resource_url,
            'credentials': credentials
        }

        if params:
            kwargs.update({'params': params})
        if data:
            kwargs.update({'data': json.dumps(data)})

        response = cls._post(**kwargs)

        if not response.ok:
            raise MercadoLibreException(response.content)

        return cls.build_object_from_dict(
            response.json(), credentials=credentials)

    @classmethod
    def get_credentials(cls, credentials=None):
        return credentials or getattr(cls, 'credentials', None)

    @classmethod
    def get_session(cls, credentials=None):
        credentials = cls.get_credentials(credentials)
        return http.get_session(credentials=credentials)

    @classmethod
    def get_detail(cls, id, params=None, credentials=None):
        resource_url = cls.get_detail_resource_endpoint(id=id)
        kwargs = {
            'url': resource_url,
            'credentials': credentials
        }

        if params:
            kwargs['params'] = params

        response = cls._get(**kwargs)

        if not response.ok:
            response.raise_for_status()

        return cls.build_object_from_dict(
            response.json(), credentials=credentials)

    @classmethod
    def get_collection(cls, iterator_resource_class=None, sub_resource=None,
                       params=None, credentials=None):
        if params is None:
            params = {}

        resource_uri = cls.get_collection_resource_endpoint(sub_resource)

        IteratorClass = cls.get_iterator_for_collection()

        return IteratorClass(
            iterator_resource_class or cls, resource_uri,
            params=params, credentials=credentials)

    def get_resource_uri(self):
        """Normalized URI for resources.
        Format: 'https://api.mercadolibre.com/[RESOURCE_NAME]/[ID]/'
        It always has a slash at the end.
        """
        if not self.id:
            raise AttributeError("Unbounded Item doesn't have an ID.")

        uri = self.get_detail_resource_endpoint(self.id)
        return uri if uri[-1] == "/" else uri + "/"

    def is_subresource(self):
        return False

    def __init__(self, *args, **kwargs):
        self.credentials = kwargs.get('credentials')
        self.session = BaseResource.get_session(
            credentials=self.credentials)

        if 'data' in kwargs:
            for name, value in kwargs.get('data').items():
                setattr(self, name, value)

    def __getattr__(self, name):
        if hasattr('self', '_data') and name in self._data:
            return self._data.get(name)
        raise AttributeError('No attribute: {0}'.format(name))


class SearchableResourceMixin(object):
    @classmethod
    def get_iterator_for_collection(cls):
        from .iterators import SearchableIterator
        return SearchableIterator

    @classmethod
    def search(cls, q=None, category_id=None, nickname=None, seller_id=None,
               offset=None, limit=None, sort_by=None, credentials=None):
        kwargs = {
            'sub_resource': 'search',
            'iterator_resource_class': ItemResource
        }
        params = {}
        available_params = [
            ('q', q), ('category', category_id), ('nickname', nickname),
            ('seller_id', seller_id), ('offset', offset), ('limit', limit),
            ('sort_by', sort_by),
        ]
        for name, value in available_params:
            if value is not None:
                params[name] = value

        if params:
            kwargs['params'] = params

        if credentials:
            kwargs['credentials'] = credentials

        return cls.get_collection(**kwargs)


class BaseSubResource(BaseResource):
    def is_subresource(self):
        return True


class ItemResource(BaseResource):
    RESOURCE_NAME = 'items'

    def get_category(self):
        if not self.category_id:
            raise AttributeError("This item doesn't have a category")
        kwargs = {
            'id': self.category_id
        }
        if self.credentials:
            kwargs['credentials'] = self.credentials

        return CategoryResource.get(**kwargs)

    category = property(get_category)

    def add_description(self, description):
        resource_uri = self.get_resource_uri() + "descriptions"
        params = {
            'access_token': self.access_token
        }

        data = {
            'text': description
        }
        kwargs = {
            'url': resource_uri,
            'data': json.dumps(data),
            'params': params
        }

        response = http.get_session().post(**kwargs)
        if not response.ok:
            response.raise_for_status()
        return response.json()


class ItemDescriptionResource(BaseSubResource):
    RESOURCE_NAME = 'items/{item_id}/descriptions'


class SiteResource(BaseResource):
    pass


class MLASiteResource(SearchableResourceMixin, SiteResource):
    RESOURCE_NAME = 'sites/MLA'


class CategoryResource(BaseResource):
    RESOURCE_NAME = 'categories'


class UserResource(BaseResource):
    RESOURCE_NAME = 'users'


class TestUser(BaseResource):
    RESOURCE_NAME = 'users/test_user'
