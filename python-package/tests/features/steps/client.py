from behave import *


@given("I have an ASA client")
def step_impl(context):
    pass


@then(u'the API_VERSION should be "{value}"')
def step_impl(context, value):
    assert context.soccer.API_VERSION == value


@then(u'the BASE_URL should be "{value}"')
def step_impl(context, value):
    assert context.soccer.BASE_URL == value


@then(u'"{league}" should be in LEAGUES')
def step_impl(context, league):
    print(context.soccer.LEAGUES)
    assert league in context.soccer.LEAGUES
