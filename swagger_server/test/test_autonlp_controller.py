# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.auto_ner_result_dto import AutoNerResultDto  # noqa: E501
from swagger_server.test import BaseTestCase


class TestAutonlpController(BaseTestCase):
    """AutonlpController integration test stubs"""

    def test_auto_ner(self):
        """Test case for auto_ner

        Convenience endpoint that delegates work to either estnlp or genericnlp tools based on input language.
        """
        body = ['body_example']
        response = self.client.open(
            '/autonlp/ner',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
