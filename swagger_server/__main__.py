#!/usr/bin/env python3
import os

import connexion

from swagger_server import encoder

port = int(os.environ.get("PORT", 8080))

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'NLP API'}, pythonic_params=True)
    app.run(port=port)


if __name__ == '__main__':
    main()
