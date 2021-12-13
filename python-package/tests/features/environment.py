from itscalledsoccer.client import AmericanSoccerAnalysis


def before_all(context):
    context.soccer = AmericanSoccerAnalysis()