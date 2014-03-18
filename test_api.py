from mercadolibre import api


APP_ID = '554056882653189'
APP_SECRET = 'a8hWBhGCbgNXhMuHrZM8nmGXLRL6wpXc'
ACCESS_TOKEN = "APP_USR-554056882653189-031816-50da07536429acf9d44587d7a488fa1b__H_F__-82365164"

img = "http://lpnk.com.ar/Publicaciones_Mercado_Libre/Datos_de_la_Empresa.jpg"
data = {
    'title': 'TEST HP CARTUCHO 122 COLOR (CH562HL)',

    'price': 188,
    "currency_id": "ARS",

    "category_id": "MLA32198",
    "available_quantity": 3,

    "buying_mode": "buy_it_now",
    "accepts_mercadopago": True,
    "listing_type_id": "bronze",
    "condition": "new",
    "warranty": "Garantia oficial HP Argentina.",

    "description": "Super description <img src={img} />".format(img=img),
    "pictures": [
        {"source": "http://mla-s2-p.mlstatic.com/pantalla-display-lenovo-g450-460-470-140-led-hd-wide-4484-MLA4914380959_082013-O.jpg"},
    ],

    "non_mercado_pago_payment_methods": [
        {
            "id": "MLATB",
            "description": "Transferencia bancaria",
            "type": "G",
        },
        {
            "id": "MLAOT",
            "description": "Tarjeta de crédito",
            "type": "N",
        },
        {
            "id": "MLAWC",
            "description": "Acordar con el comprador",
            "type": "G",
        },
        {
            "id": "MLAMO",
            "description": "Efectivo",
            "type": "G",
        },
    ],
}
from mercadolibre.resources import Category

ml = api.login(APP_ID, APP_SECRET)
redirect_url = "http://localhost:8000/callbacks/auth/ml/"
auth_url = ml.build_authorization_url(redirect_url)
print(auth_url)
exit()

# item = ml.create_item(data=data)
response = ml.site.search("HP CARTUCHO 122 COLOR")
results = response.get('results')

for result in results[:1]:
    item = ml.items.get(id=result.get('id'))
    category = item.category
    cat_title = ""
    for parent in category.path_from_root:
        cat_title += "{name}({id}) > ".format(
            name=parent['name'], id=parent['id'])

    cat_title += "{0}({1})".format(category.name, category.id)
    print(cat_title)


# resp = client.validate_item(data)
# code = resp.status_code
# assert code == 204
# item = client.create_item(data)
# import ipdb; ipdb.set_trace()


#item = client.create_item(data)
test_data = {'accepts_mercadopago': True,
             'attributes': [],
             'automatic_relist': False,
             'available_quantity': 3,
             'base_price': 188,
             'buying_mode': 'buy_it_now',
             'catalog_product_id': None,
             'category_id': 'MLA32198',
             'condition': 'new',
             'coverage_areas': [],
             'currency_id': 'ARS',
             'date_created': '2014-03-14T19:02:17.342Z',
             'descriptions': [],
             'end_time': '2014-05-13T19:02:16.854Z',
             'geolocation': {'latitude': '', 'longitude': ''},
             'id': 'MLA499176256',
             'initial_quantity': 3,
             'last_updated': '2014-03-14T19:02:17.342Z',
             'listing_source': '',
             'listing_type_id': 'bronze',
             'location': {},
             'non_mercado_pago_payment_methods': [],
             'official_store_id': None,
             'parent_item_id': None,
             'permalink': 'http://articulo.mercadolibre.com.ar/MLA-499176256-hp-cartucho-122-color-ch562hl-_JM',
             'pictures': [],
             'price': 188,
             'secure_thumbnail': '',
             'seller_address': {'address_line': '66 nro 415 1 A',
                                'city': {'id': 'TUxBQ1JBVzEyY2Ey',
                                         'name': 'Rawson'},
                                'comment': '',
                                'country': {'id': 'AR', 'name': 'Argentina'},
                                'id': 75820774,
                                'latitude': '',
                                'longitude': '',
                                'search_location': {
                                    'city': {'id': '', 'name': ''},
                                    'neighborhood': {'id': '',
                                                     'name': ''},
                                    'state': {'id': '', 'name': ''}},
                                'state': {'id': 'AR-U', 'name': 'Chubut'},
                                'zip_code': ''},
             'seller_contact': None,
             'seller_custom_field': None,
             'seller_id': 82365164,
             'shipping': {'dimensions': None,
                          'free_shipping': False,
                          'local_pick_up': False,
                          'methods': [],
                          'mode': 'not_specified'},
             'site_id': 'MLA',
             'sold_quantity': 0,
             'start_time': '2014-03-14T19:02:16.854Z',
             'status': 'not_yet_active',
             'stop_time': '2014-05-13T19:02:16.854Z',
             'sub_status': [],
             'subtitle': None,
             'tags': [],
             'thumbnail': '',
             'title': 'Hp Cartucho 122 Color (ch562hl)',
             'variations': [],
             'video_id': None,
             'warranty': 'Garantia oficial HP Argentina.'}

# item = Item(client, test_data)
# img = "http://lpnk.com.ar/Publicaciones_Mercado_Libre/Datos_de_la_Empresa.jpg"
# resp = item.add_description(
#     "Super description <img src={img} />".format(img=img)
# )

#import ipdb; ipdb.set_trace()
# http://articulo.mercadolibre.com.ar/MLA-499176256-hp-cartucho-122-color-ch562hl-_JM

