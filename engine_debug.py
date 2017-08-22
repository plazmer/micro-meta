import os
import sys
import plugin
import utils
from plugins.dmir import request, parse

query = "компрессор"

params = plugin.default_params()
req = request(query, params, None)
print(req)

html = utils.http(req)
for r in parse(html):
	print(r)