# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.est_ner_result_dto import EstNerResultDto  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEstnlpController(BaseTestCase):
    """EstnlpController integration test stubs"""

    def test_est_ner(self):
        """Test case for est_ner

        Helps with named entity recognition using estnltk. Extended to also include temporal info.
        """
        body = ['body_example']
        response = self.client.open(
            '/estnlp/ner',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
