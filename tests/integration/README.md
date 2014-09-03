# Integration tests

These tests use [VCR.py](https://github.com/kevin1024/vcrpy) to test the proper handling of the SDK with the actual ML api.

Most of the tests in this suite will need a valid access token. We recommend you to use a test user (you can create it with the `simple_client.py` script included in this package). The tests will try to get the access token from your enviroment variables. If you're using some variation of *nix you can do:

    $ ML_TESTING_ACCESS_TOKEN=APP_USR-XXX-090314-85c2a498bf6e75b003008c70d1c071bd__N_J__-165949089 py.test tests/integration/

There's also another envvar used to control the record mode of `vcrpy` (for more details check their docs). It's called `ML_TESTS_RECORD_MODE`. Values can be: `(all|once|none|new_episodes)` (`once` is used by default).

### Running integration tests

Integration tests are marked as `integration` using [py.test metadata marking](http://pytest.org/latest/example/markers.html). So you just have to do:

    $ py.test -m integration tests

If you want to run all tests EXCEPT integration tests you can:

    $ py.test -m "not integration" tests  # Note the "not integration" mark.

BTW, [py.test](http://pytest.org) is pure magic.