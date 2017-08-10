import os
import sys
import plugin
from plugins.irr import request, parse

query = "холодильник"

params = plugin.default_params
req = request(query, params, None)
print(req)

html = plugin.http(req)

print(parse(html['page']))
