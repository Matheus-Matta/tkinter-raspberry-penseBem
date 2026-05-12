import re
import os

books = ['021', '081', '131']
output = "gabaritos = {\n"

for book in books:
    with open(f"./src/gabarito/{book}.ts", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract the programs
    output += f'    "{book}": {{\n'
    for prog in range(1, 6):
        prog_name = f'programa_{prog}'
        # find the list inside [ ... ]
        pattern = r'{}:\s*\[(.*?)\]'.format(prog_name)
        match = re.search(pattern, content, re.DOTALL)
        if match:
            items_str = match.group(1)
            output += f'        "{prog_name}": [\n'
            
            # find all { questao: X, cor: "Y", resposta: "Z" }
            items = re.findall(r'{[^{}]*}', items_str)
            for item in items:
                # convert JS object to Python dict
                item = re.sub(r'questao:\s*(\d+)', r'"questao": \1', item)
                item = re.sub(r'cor:\s*(".*?")', r'"cor": \1', item)
                item = re.sub(r'resposta:\s*(".*?")', r'"resposta": \1', item)
                output += f'            {item},\n'
            
            output += '        ],\n'
    output += '    },\n'

output += "}\n"

with open("gabarito_data.py", "w", encoding="utf-8") as f:
    f.write(output)
print("gabarito_data.py generated successfully.")
