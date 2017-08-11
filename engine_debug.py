import os
import sys
import plugin
from plugins.doski import request, parse

query = "компрессор"

params = plugin.default_params()
req = request(query, params, None)
print(req)

html = plugin.http(req)

print(parse(html['page']))
