from behave import *
from itscalledsoccer.client import AmericanSoccerAnalysis

@then(u'the API_VERSION should be "{value}"')
def step_impl(context, value):
    assert context.soccer.API_VERSION == value

@then(u'the BASE_URL should be "{value}"')
def step_impl(context, value):
    assert context.soccer.BASE_URL == value

@then(u'the MAX_API_LIMIT should be "{value}"')
def step_impl(context, value):
    assert context.soccer.MAX_API_LIMIT == int(value)

@then(u'"{league}" should be in LEAGUES')
def step_impl(context, league):
    print(context.soccer.LEAGUES)
    assert league in context.soccer.LEAGUES

@then(u'there is a logger')
def step_impl(context):
    assert context.soccer.LOGGER is not None

@then(u'the logging level is WARNING')
def step_impl(context):
    assert context.soccer.LOGGER.getEffectiveLevel() == 30

@then(u'the logging level is DEBUG')
def step_impl(context):
    assert context.soccer.LOGGER.getEffectiveLevel() == 10

@when(u'the logging level is set to "{level}"')
def step_impl(context, level):
    context.soccer = AmericanSoccerAnalysis(logging_level=level)

@when(u'the proxy is set to "{url}"')
def step_impl(context, url):
    proxies = {
        "http": f"http://{url}",
        "https": f"https://{url}"
    }
    context.soccer = AmericanSoccerAnalysis(proxies=proxies)

@then(u'the session is using a proxy')
def step_impl(context):
    proxies = {
    'http': 'http://10.10.1.10:3128',
    'https': 'http://10.10.1.10:1080',
    }
    assert context.soccer.SESSION.proxies == proxies