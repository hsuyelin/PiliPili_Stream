#!/usr/bin/env python3

# -*- coding: utf-8 -*-


from flask_cors import CORS

from app import app

# noinspection SpellCheckingInspection
CORS(app, resources={r"/*": {"origins": "*"}})


if __name__ == "__main__":
    app.run(port=60001, debug=True, host="0.0.0.0", threaded=True)
