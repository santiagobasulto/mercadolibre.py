from __future__ import unicode_literals
import json

import click

from mercadolibre import api


def capitalize(s):
    return s[0].upper() + s[1:]


def log_api_object(obj, props):
    for prop in props:
        click.echo(
            "\t{0}: {1}".format(capitalize(prop), getattr(obj, prop)))


class State(object):

    def __init__(self):
        self.app_id = None
        self.app_secret = None
        self.access_token = None
        self.site_id = None

pass_state = click.make_pass_decorator(State, ensure=True)


def app_id_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.app_id = value
        return value
    return click.option(
        '--app-id', type=click.STRING, help='MercadoLibre APP ID.',
        envvar='ML_APP_ID', callback=callback)(f)


def app_secret_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.app_secret = value
        return value
    return click.option(
        '--app-secret', type=click.STRING, help='MercadoLibre APP SECRET.',
        envvar='ML_APP_SECRET', callback=callback)(f)


def access_token_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.access_token = value
        return value
    return click.option(
        '--access-token', type=click.STRING, help='MercadoLibre ACCESS TOKEN.',
        callback=callback)(f)


def site_id_option(f):
    def callback(ctx, param, value):
        state = ctx.ensure_object(State)
        state.site_id = value
        return value
    return click.option(
        '--site-id', type=click.Choice(['MLA', 'MLB', 'MLM']), default='MLA',
        callback=callback)(f)


def common_options(f):
    f = app_id_option(f)
    f = app_secret_option(f)
    f = access_token_option(f)
    f = site_id_option(f)
    return f


@click.group()
@common_options
@pass_state
def main(state, **kwargs):
    if not all([state.app_id, state.app_secret]):
        raise click.UsageError("You must provide an app_id and an app_secret")


@main.command()
@common_options
@pass_state
def create_test_user(state, **kwargs):
    if not state.access_token:
        raise click.UsageError("This method requires an ACCESS TOKEN")

    ml = api.login(
        app_id=state.app_id, app_secret=state.app_secret,
        access_token=state.access_token)

    test_user = ml.test_user.post({'site_id': state.site_id})
    click.echo("Test user created.")
    log_api_object(test_user, ['id', 'nickname', 'password', 'email'])
    click.echo("")


@main.command()
@click.argument('input', type=click.File('r'))
@common_options
@pass_state
def create_test_item(state, input, **kwargs):
    if not state.access_token:
        raise click.UsageError("This method requires an ACCESS TOKEN")
    data = json.loads(input.read())
    ml = api.login(
        app_id=state.app_id, app_secret=state.app_secret,
        access_token=state.access_token)
    item = ml.items.post(data=data)

    click.echo("Test Item created.")
    log_api_object(item, ['id', 'permalink'])
    click.echo("")


@main.command()
@click.argument('item_id')
@click.option('-c', '--include-category', is_flag=True, default=False)
@common_options
@pass_state
def get_item(state, item_id, include_category, **kwargs):
    if not state.access_token:
        raise click.UsageError("This method requires an ACCESS TOKEN")

    ml = api.login(
        app_id=state.app_id, app_secret=state.app_secret,
        access_token=state.access_token)
    item = ml.items.get(id=item_id)
    click.echo("Test Item created.")
    log_api_object(item, ['id', 'permalink'])
    click.echo("")

    if include_category:
        category = item.category
        click.echo("Category Info:")
        log_api_object(category, ['id', 'name', 'path_from_root'])
    click.echo("")


@main.command()
@common_options
@pass_state
def me(state, **kwargs):
    if not state.access_token:
        raise click.UsageError("This method requires an ACCESS TOKEN")

    ml = api.login(
        app_id=state.app_id, app_secret=state.app_secret,
        access_token=state.access_token)

    me = ml.me()
    click.echo("Test user created.")
    log_api_object(me, ['id', 'nickname', 'email'])
    click.echo("")


@main.command()
@click.option('-q', '--query', help="The querystring to search for")
@click.option('-c', '--category-id',
              help="The ID of the category to restrict your search")
@click.option('-n', '--nickname',
              help="Nickname of the seller you want to search items from")
@common_options
@pass_state
def search(state, query, category_id, nickname, **kwargs):
    ml = api.login(
        app_id=state.app_id, app_secret=state.app_secret,
        access_token=state.access_token)
    search = ml.mla.search(q=query, category_id=category_id, nickname=nickname)
    result_txt = "result{0}".format(((search.total_count > 1 and "s") or ""))
    click.echo(
        "Your search returned {0} {1}.".format(search.total_count, result_txt))

if __name__ == '__main__':
    main()
