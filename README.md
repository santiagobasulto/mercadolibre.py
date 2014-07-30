## mercadolibre.py

Improved Python client for MercadoLibre API.

### Simple CLI client. Test the API by your own.

I've created a simple CLI client to ease your testing and development. It's also a great example of how to use `mercadolibre.py`.

```bash
# Create a test user
$ python simple_client.py create_test_user --access-token YOUR_ACCESS_TOKEN

# Create a test Item from a file called data.json
$ python simple_client.py create_test_item data.json --access-token YOUR_ACCESS_TOKEN

# Search all items containing the string "Jawbone Up24"
$ python simple_client.py search -q "Jawbone Up24"
```

To use it you'll need an `APP_ID`, an `APP_SECRET` and (sometimes) an `ACCESS_TOKEN`. You'll find more information on how to get them on the [MercadoLibre documentation site](http://developers.mercadolibre.com/first-step/).

To make your life easier you can configure your client to get your `APP_ID` and `APP_SECRET` from envvars. Just issue these commands (or add them to your `.bashrc` or similar). Example:

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

**Search**

```bash

# By Querystring
$ python simple_client.py search -q "Jawbone Up24"

# By Querystring and Category ID
$ python simple_client.py search -q "Jawbone Up24" -c MLA12272

# By Category ID
$ python simple_client.py search -c MLA12272

# By Seller Nickname
$ python simple_client.py search -n "LAPLATA-NOTEBOOKS"

# By Seller ID
$ python simple_client.py search -s 38726013

```

## Run tests

```bash
# -s doesn't captures output. You'll be able to ipdb and print in your tests.
$ py.test -s tests/resources/test_items.py::ItemResourceHighLevelTestCase::test_some_method
```
