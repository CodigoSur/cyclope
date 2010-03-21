"""Theme configurations."""

import os

# hacky stuff...

# skip __init.py and __init__.pyc
available = [ item for item in os.listdir(
    os.path.join(os.path.dirname(__file__))
    )
             if not item.startswith('__init__.py')]

for theme in available:
    exec 'import %s' % theme
