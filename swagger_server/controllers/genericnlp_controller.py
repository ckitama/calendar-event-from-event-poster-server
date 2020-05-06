import connexion
import six

from swagger_server.api import genericnlp_api
from swagger_server.models.generic_ner_result_dto import GenericNerResultDto  # noqa: E501
from swagger_server import util


def generic_ner(body):  # noqa: E501
    """Helps with named entity recognition using SpaCy. Additionaly uses TextBlob to detect input text&#x27;s language and translate it to English if necessary (as SpaCy only works with English).

     # noqa: E501

    :param body: Input text in any language
    :type body: List[]

    :rtype: GenericNerResultDto
    """
    return genericnlp_api.find_generic_ner(body)
