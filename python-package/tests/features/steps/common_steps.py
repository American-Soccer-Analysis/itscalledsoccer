from behave import *
from pandas import DataFrame


@given("there is an ASA client")
def step_impl(context):
    pass

@then("there is data")
def step_impl(context):
    assert context.response is not None
    assert isinstance(context.response, DataFrame)
    assert len(context.response) >= 1