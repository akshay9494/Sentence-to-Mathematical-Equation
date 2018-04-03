from flask_restplus import Api
from .equation_solver import api as ns1


api = Api(
    title='Math equation solver for Chatbot',
    version='1.0'
    # All API metadatas
)

api.add_namespace(ns1)