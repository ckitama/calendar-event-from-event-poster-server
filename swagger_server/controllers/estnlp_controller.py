import connexion
import six

from swagger_server.api import estnlp_api
from swagger_server.models.est_ner_result_dto import EstNerResultDto  # noqa: E501
from swagger_server import util


def est_ner(body):  # noqa: E501
    """Helps with named entity recognition using estnltk. Extended to also include temporal info.

     # noqa: E501

    :param body: Input text in Estonian
    :type body: List[]

    :rtype: EstNerResultDto
    """
    return estnlp_api.find_est_ner(body)
