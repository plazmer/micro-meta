import os
import sys
import plugin
from plugins.doski import request, parse

query = "bitzer"

params = plugin.default_params()
req = request(query, params, None)
print(req)

html = plugin.http(req)
for r in parse(html['page']):
	print(r['photo'])