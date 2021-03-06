from pyoptix.context import current_context
from pyoptix.mixins.destroyable import DestroyableObject
from pyoptix.mixins.graphnode import GraphNodeMixin
from pyoptix.mixins.parent import ParentMixin
from pyoptix.mixins.hascontext import HasContextMixin


class Group(GraphNodeMixin, ParentMixin, HasContextMixin, DestroyableObject):
    def __init__(self, children=None):
        from pyoptix.acceleration import Acceleration
        from pyoptix.geometry_group import GeometryGroup
        from pyoptix.selector import Selector
        from pyoptix.transform import Transform

        HasContextMixin.__init__(self, current_context())
        DestroyableObject.__init__(self, self._safe_context._create_group())
        GraphNodeMixin.__init__(self)
        ParentMixin.__init__(self, [GeometryGroup, Group, Selector, Transform, Acceleration], children)

        self._acceleration = None

    def set_acceleration(self, acceleration):
        try:
            acceleration.validate()
        except Exception as e:
            raise RuntimeError('Acceleration could not be validated')

        self._safe_native.set_acceleration(acceleration._safe_native)
        self._acceleration = acceleration

    def get_acceleration(self):
        return self._acceleration

    def validate(self):
        self._safe_native.validate()

    """
    Use Context scope when a variable is assigned to GeometryGroup
    """
    def __getitem__(self, item):
        return self._safe_context[item]

    def __setitem__(self, key, value):
        if value is not None:
            self._safe_context[key] = value

    def __delitem__(self, key):
        del self._safe_context[key]

    def __contains__(self, item):
        return item in self._safe_context
