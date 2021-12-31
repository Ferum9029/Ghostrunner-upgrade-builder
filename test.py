from field import Field, generate_field_id
from upgrades import upgrades
import json

upgrade = upgrades[0]
upgrade.rotate()
upgrade.rotate()
field_ = Field(json.loads(open('jsons/field.json', 'r').read())['field'])
field_.place_figure(upgrade.shape, 2, 4)
print(generate_field_id(field_.field))
