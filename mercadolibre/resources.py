import json

from . import http
from . import config

__all__ = ['Item', 'SiteMLA', 'UserResource']


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
    def get(cls, id=None, params=None, access_token=None):
        if id:
            return cls.get_detail(id, params=params, access_token=access_token)
        else:
            return cls.get_collection(params=params, access_token=access_token)

    @classmethod
    def build_object_from_dict(cls, data_dict, access_token=None):
        data_dict.update({
            '_data': data_dict,
            'access_token': access_token
        })
        obj = cls(**data_dict)
        return obj

    @classmethod
    def post(cls, data=None, params=None, access_token=None):
        if params is None:
            params = {}
        if access_token and not 'access_token' in params:
            params.update({'access_token': access_token})

        resource_url = cls.get_collection_resource_endpoint()

        kwargs = {'url': resource_url}
        if params:
            kwargs.update({'params': params})
        if data:
            kwargs.update({'data': json.dumps(data)})

        response = http.get_session().post(**kwargs)

        if not response.ok:
            response.raise_for_status()
        return cls.build_object_from_dict(
            response.json(), access_token=access_token)

    @classmethod
    def get_detail(cls, id, params=None, access_token=None):
        if params is None:
            params = {}
        if access_token and not 'access_token' in params:
            params.update({'access_token': access_token})

        resource_url = cls.get_detail_resource_endpoint(id=id)

        kwargs = {'url': resource_url}
        if params:
            kwargs.update({'params': params})
        response = http.get_session().get(**kwargs)

        if not response.ok:
            response.raise_for_status()

        return cls.build_object_from_dict(
            response.json(), access_token=access_token)

    @classmethod
    def get_collection(cls, sub_resource=None, params=None, access_token=None):
        if params is None:
            params = {}
        if access_token and not 'access_token' in params:
            params.update({'access_token': access_token})

        resource_url = cls.get_collection_resource_endpoint(sub_resource)

        kwargs = {'url': resource_url}
        if params:
            kwargs.update({'params': params})

        response = http.get_session().get(**kwargs)
        if not response.ok:
            response.raise_for_status()

        # TODO: Build objects or iterator
        return response.json()

    def get_resource_uri(self):
        """Normalized URI for resources.
        Format: 'https://api.mercadolibre.com/[RESOURCE_NAME]/[ID]/'
        It always has a slash at the end.
        """
        if not self.id:
            raise AttributeError("Unbounded Item doesn't have an ID.")

        uri = self.get_detail_resource_endpoint(self.id)
        return uri if uri[-1] == "/" else uri + "/"

    def __init__(self, *args, **kwargs):
        self.session = http.get_session()
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __getattr__(self, name):
        if hasattr('self', '_data') and name in self._data:
            return self._data.get(name)
        raise AttributeError('No attribute: {0}'.format(name))


class Item(BaseResource):
    RESOURCE_NAME = 'items'

    def get_category(self):
        if not self.category_id:
            raise AttributeError("This item doesn't have a category")
        return Category.get(id=self.category_id)

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



class SiteMLA(BaseResource):
    RESOURCE_NAME = 'sites/MLA'

    @classmethod
    def search(cls, q, access_token=None):
        return cls.get_collection('search', params={'q': q})


class Category(BaseResource):
    RESOURCE_NAME = 'categories'


class UserResource(BaseResource):
    RESOURCE_NAME = 'users'