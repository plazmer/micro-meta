import os
import sys
import plugin
import utils
from plugins.avito import request, parse

query = "труба нержавеющая"

params = plugin.default_params()
req = request(query, params, None)
print(req)

html = utils.http(req)
for r in parse(html):
	print(r['photo'])