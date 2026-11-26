from pathlib import Path
import json
from jsonschema import Draft202012Validator
root=Path(__file__).parent
count=0
for file in sorted((root/'examples').glob('*.example.json')):
    name=file.name.removesuffix('.example.json')
    schema=json.loads((root/'schemas'/f'{name}.schema.json').read_text(encoding='utf-8'))
    data=json.loads(file.read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(data)
    count += 1
print(f'Validated {count} example files against JSON Schema Draft 2020-12')
