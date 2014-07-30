## mercadolibre.py

Improved Python client for MercadoLibre API.

### Simple CLI client. Test the API by your own.

I've included a simple command line client to interact with the API. There are a number of commands included. You can always include yours. Just send your PRs.

To use it you'll need an APP_ID, an APP_SECRET and an ACCESS_TOKEN. You'll find more information to get it on the [MercadoLibre documentation site](http://developers.mercadolibre.com/first-step/). Once you have those tokens you should first **create a test user** so you won't hurt your own private user.

To make your life easier you can configure your client to get your APP_ID and APP_SECRET from envvars. Just issue these commands (or add them to your `.bashrc` or similar).

```bash
$ export ML_APP_ID=999-YOUR_APP_ID-999
$ export ML_APP_SECRET=999-YOUR_APP_SECRET-999
```

**Create a test user using the client**

```bash
$ python simple_client.py create_test_user --access-token YOUR_ACCESS_TOKEN
```

**Create an item**
You'll need to provide the data for your item in a json file (or you could just `cat` it because it reads from stdin).

```bash
$ python simple_client.py create_test_item data.json --access-token YOUR_ACCESS_TOKEN
```

**Search*
```bash

# By Querystring
$ python simple_client.py search -q "Jawbone Up24"

# By Querystring and Category ID
$ python simple_client.py search -q "Jawbone Up24" -c MLA12272

# By Category ID
$ python simple_client.py search -c MLA12272

# By Seller Nickname
$ python simple_client.py search -n "LAPLATA-NOTEBOOKS"

```

## Run tests

py.test -s tests/resources/test_items.py::ItemResourceHighLevelTestCase