from pyoddgen.config import create_default_project_config
from pyoddgen.manager import GeneratorManager

config = create_default_project_config()
manager = GeneratorManager(config)
print(manager)
manager.start_generation()
