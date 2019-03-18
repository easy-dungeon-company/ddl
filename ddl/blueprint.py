"""
Blueprints
"""

import json
import logging

from ddl.validator import Validator


DEFAULT_FLOORMAP = {
    'floor': 0,
    'wall':  1,
    'prop':  2
}


class BlueprintFactory:
    """Create a Blueprint from a JSON file"""

    @staticmethod
    def load(name):
        """Loads AssetPacks from their component and Image packs,
         given an appropriate name"""

        logger = logging.getLogger('ddl')

        with open(name) as blueprint_file:
            blueprint_json = json.load(blueprint_file)

            # Test this JSON is valid
            Validator.validate_json(blueprint_json, 'blueprint')

            blueprint = Blueprint()

            for part in blueprint_json['parts']:
                # top_left_x=
                # "x": 0,
                # "y": 0,
                # "width": 3,
                # "height": 3,
                # "layer": "floor",
                # "constraints": [
                #     "floor"
                # ]

                if not part['width']:
                    part['width'] = 1

                if not part['height']:
                    part['height'] = 1

                logger.debug('Adding {} range constraints for ({}, {}) on layer "{}" with width {} and height {}: {}'.format(len(part['constraints']), part['x'], part['y'], part['layer'], part['width'], part['height'], ', '.join(part['constraints'])))

                blueprint.add_range_constraint(
                    x=part['x'],
                    y=part['y'],
                    width=part['width'],
                    height=part['height'],
                    layer=part['layer'],
                    constraints=part['constraints']
                )

            # The file is valid, pass it along to a blueprint
            return blueprint


class Blueprint:
    """ A collection of constraints as applied to a grid. """

    def __init__(self):

        self.layers = {}
        self.logger = logging.getLogger('ddl')

    def add_tile_constraint(self, x, y, layer, constraints):

        self.logger.debug('Adding {} tile constraints to layer "{}" at ({}, {}): {}'.format(len(constraints), layer, x, y, ', '.join(constraints)))

        layer = self.layers.setdefault(layer, {})

        if (x, y) in layer:
            layer[(x, y)] = layer[(x, y)] + constraints
        else:
            layer[(x, y)] = constraints

    def add_range_constraint(self, x, y, layer, width, height, constraints):
        for final_x, final_y in ((x, y) for x in range(width) for y in range(height)):
            self.add_tile_constraint(x + final_x, y + final_y, layer, constraints)

    def get_constraints_in_layer(self, layer):
        if layer not in self.layers:
            raise Exception("That layer doesn't exist")

        return(self.layers[layer])
