import connexion
import six

from swagger_server.api import autonlp_api
from swagger_server.models.auto_ner_result_dto import AutoNerResultDto  # noqa: E501
from swagger_server import util


def auto_ner(body):  # noqa: E501
    """Convenience endpoint that delegates work to either estnlp or genericnlp tools based on input language.

     # noqa: E501

    :param body: Input text in any language
    :type body: List[]

    :rtype: AutoNerResultDto
    """
    return autonlp_api.find_auto_ner(body)
