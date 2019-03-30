import gettext
import os

from os.path import dirname

# _ROOT_DIR points to the root directory of the GRASS installation/distribution
# Yeap, calling 4 times dirname is not really elegant, but we want to go from:
#     dist.x86_64-pc-linux-gnu/etc/python/grass/__init__.py
# to:
#     dist.x86_64-pc-linux-gnu/
#
_ROOT_DIR = dirname(dirname(dirname(dirname(os.path.abspath(__file__)))))

# Setup i18N
#
# Calling `gettext.install()` injects `_()` in the builtins namespace and
# thus it becomes available globally (i.e. in the same process). Any python
# code that needs to use _() should make sure that it firsts imports this
# library.
#
# Note: we need to do this at the beginning of this module in order to
# ensure that the injection happens before anything else gets imported.
#
# For more info please check the following links:
# - https://docs.python.org/2/library/gettext.html#gettext.install
# - https://pymotw.com/2//gettext/index.html#application-vs-module-localization
# - https://www.wefearchange.org/2012/06/the-right-way-to-internationalize-your.html
#
_LOCALE_DIR = os.path.join(_ROOT_DIR, 'locale')
gettext.install('grasslibs', _LOCALE_DIR)
gettext.install('grassmods', _LOCALE_DIR)
gettext.install('grasswxpy', _LOCALE_DIR)


__all__ = ["script", "temporal"]
if os.path.exists(os.path.join(os.path.dirname(__file__), "lib", "__init__.py")):
    __all__.append("lib")
