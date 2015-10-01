from pyoptix._driver import _OptixMaterialWrapper
from pyoptix.objects.commons.optix_object import OptixObject
from pyoptix.objects.commons.optix_scoped_object import OptixScopedObject


class OptixMaterial(_OptixMaterialWrapper, OptixObject, OptixScopedObject):

    def __init__(self, native, context):
        OptixObject.__init__(self, context, native)
        _OptixMaterialWrapper.__init__(self, native)
        OptixScopedObject.__init__(self)

        self._closest_hit_programs = {}
        self._any_hit_programs = {}

    def set_closest_hit_program(self, ray_type_index, program):
        self._closest_hit_programs[ray_type_index] = program
        self._set_closest_hit_program(ray_type_index, program)

    def get_closest_hit_program(self, ray_type_index):
        return self._closest_hit_programs[ray_type_index]

    def set_any_hit_program(self, ray_type_index, program):
        self._any_hit_programs[ray_type_index] = program
        self._set_any_hit_program(ray_type_index, program)

    def get_any_hit_program(self, ray_type_index):
        return self._any_hit_programs[ray_type_index]
