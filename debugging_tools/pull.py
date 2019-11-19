import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import urllib.error
import re
from paradoxReader import decode
import json
import asyncpg
import asyncio


with open('Backup0.txt.json', 'r') as f:
    fhand = f.read()
    data = json.loads(fhand)
#
# for x, y in data.items():
#     x = x.replace("_idea_groups_expanded", "").replace("_", " ").title()
#     print(x)
#     for a,b in y.items():
#         b = str(b).replace("{", "").replace("}", "").replace("'", "")
#         a = a.replace("_", " ").title()
#         if a == 'Category':
#             temp = f'     {a}: {b}'
#
#             print(temp)
#         else:
#             print("     " + a)
#             print("          " + b )

#
decode('Backup0.txt', None, None)
