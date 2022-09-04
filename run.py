#!/usr/bin/env python
from app import app
app.run(debug=True, ssl_context=('../cert.pem', '../key.pem'))

#, ssl_context=('../cert.pem', '../key.pem') to run locally.
