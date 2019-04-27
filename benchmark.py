import shlex
import subprocess

from grass.pygrass.modules import Module
import grass.script as gscript
from grass.pygrass.modules.shortcuts import raster as r

import timer

### START Python module

def pygrass_module_p():
    module = Module("r.simple")
    return module(input="elevation", output="foo")


def pygrass_shortcut_p():
    return r.simple(input="elevation", output="foo")


def grass_script_p():
    return gscript.run_command("r.simple", input="elevation", output="foo")


def subprocess_call_p():
    return subprocess.check_call(shlex.split("r.simple input=elevation output=foo"))

### END Python module

### START C module

def pygrass_module_c():
    module = Module("r.simple.c")
    return module(input="elevation", output="foo")


def pygrass_shortcut_c():
    return r.simple_c(input="elevation", output="foo")


def grass_script_c():
    return gscript.run_command("r.simple.c", input="elevation", output="foo")


def subprocess_call_c():
    return subprocess.check_call(shlex.split("r.simple.c input=elevation output=foo"))


### END C module


def subprocess_call_plain():
    return subprocess.check_call(shlex.split("true"))


def python2_startup_time():
    return subprocess.check_call(shlex.split("python2 -c '1'"))


def python3_startup_time():
    return subprocess.check_call(shlex.split("python3 -c '1'"))


def python2_import_grass_script():
    return subprocess.check_call(shlex.split("python2 -c 'import grass.script'"))


def python3_import_grass_script():
    return subprocess.check_call(shlex.split("python3 -c 'import grass.script'"))


def run_benchmark(*functions):
    for func in functions:
        print(func.__name__)
        timer.AutoTimer(func).auto(verbose=True, repeat=10)
        print()


print()
print("### GRASS Module call overhead - Python")
print()
run_benchmark(pygrass_module_p, pygrass_shortcut_p, grass_script_p, subprocess_call_p)

print()
print("### GRASS Module call overhead - C")
print()
run_benchmark(pygrass_module_c, pygrass_shortcut_c, grass_script_c, subprocess_call_c)

print()
print("### Python interpreter startup time overhead")
print()
run_benchmark(subprocess_call_plain, python2_startup_time, python3_startup_time)

print()
print("### Python interpreter + `import grass.script` overhead")
print()
run_benchmark(python2_import_grass_script, python3_import_grass_script)
