import logging
from pyoptix.highlevel.shared import context

logger = logging.getLogger(__name__)


class EntryPoint(object):
    def __init__(self, ray_generation_program, exception_program=None, size=None):
        self.ray_generation_program = ray_generation_program
        self.exception_program = exception_program
        self.size = size

    def __call__(self):
        self.launch()

    def __getitem__(self, item):
        return self.ray_generation_program[item]

    def __setitem__(self, key, value):
        if value is not None:
            self.ray_generation_program[key] = value

    def __delitem__(self, key):
        del self.ray_generation_program[key]
        
    def __contains__(self, item):
        return item in self.ray_generation_program

    def launch(self, size=None):
        if self.size is None and size is None:
            raise ValueError("Launch size must be set before or while launching")
        elif size is None:
            size = self.size

        context.set_entry_point_count(1)
        context.set_ray_generation_program(0, self.ray_generation_program)
        if self.exception_program is not None:
            context.set_exception_program(0, self.exception_program)

        # launch
        context.validate()
        context.compile()
        logger.debug("Launching {0} with {1} threads".format(self.ray_generation_program, size))
        context.launch(0, *size)