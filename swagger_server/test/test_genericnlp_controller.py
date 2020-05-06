# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.generic_ner_result_dto import GenericNerResultDto  # noqa: E501
from swagger_server.test import BaseTestCase


class TestGenericnlpController(BaseTestCase):
    """GenericnlpController integration test stubs"""

    def test_generic_ner(self):
        """Test case for generic_ner

        Helps with named entity recognition using spaCy. Additionaly uses TextBlob to detect input text's language and translate it to English if necessary (as spaCy works best in English).
        """
        body = ['body_example']
        response = self.client.open(
            '/genericnlp/ner',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
