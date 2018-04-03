from flask_restplus import Namespace, Resource, fields
import os
import logging
from core.s2me_response import S2MEResponse
from core.s2me import sent_to_result



api = Namespace('S2ME', description='Converts sentences to mathematical equations and solves them.')

s2me_payload = api.model('S2ME', {
    'sentence': fields.String(required=True, description='What someone would ask the chatbot to solve. '
                                                         'For ex:- how much is two plus two?')
})


s2me_response = api.model('S2ME Response', {
    'answer': fields.String(description='Answer to the mathematical equation'),
    'equation': fields.String(description='Equation formed from the sentence.')
})


@api.route('/basic_calculations')
class S2ME(Resource):
    """Ability to do basic mathematical calculations by understanding sentences."""
    @api.doc('basic mathematical computations')
    @api.expect(s2me_payload)
    @api.marshal_with(s2me_response, code=200)
    def post(self):
        """Solve mathematical equations from sentences."""
        logging.info('Received post message.')
        sentence = self.api.payload['sentence']
        logging.debug('Sentence Extracted as: {}'.format(sentence))
        equation, answer = sent_to_result(sentence)
        return S2MEResponse(equation, answer), 200
