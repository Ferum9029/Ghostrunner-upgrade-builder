import json
from dataclasses import dataclass
_upgrades_ = json.loads(open('jsons/figures.json').read())


@dataclass
class Upgrade:
    __slots__ = ('id', 'name', 'shape')
    id: int
    name: str
    shape: tuple[tuple, ...]

    def rotate(self):
        self.shape = tuple(zip(*reversed(self.shape)))


upgrades = [Upgrade(id=upgrade['id'], name=upgrade['name'], shape=upgrade['figure'])
            for upg_name in _upgrades_
            for upgrade in _upgrades_[upg_name]]
