import os
import subprocess

build_options = {
        'arch': 'Win32',
        'config': 'Release',
        'generator': 'Visual Studio 16 2019',
        'build-dir': 'build' + os.path.sep + 'arch' + os.path.sep + 'config'
    }

def set_build_directory():
    '''
    Creates the final build directory.
    Can use already defined keys from the `build_options` directory.
    Replaces any other key found in the `build_options` dictionary with its value except `build-dir`.
    '''
    components = build_options['build-dir'].split(os.path.sep)
    replaced_components = []

    for c in components:
        if c != 'build-dir' and c in build_options:
            replaced_components.append(build_options[c])
        else:
            replaced_components.append(c)

    build_options['build-dir'] = os.path.sep.join( [str(c) for c in replaced_components] )

def cmake_configure():
    cmakeCmd = [
        'cmake', 
        '-S', '.',
        '-B', build_options['build-dir'],
        '-G', build_options['generator'],
        '-A', build_options['arch'],
        '-DCMAKE_BUILD_TYPE='+build_options['config']
    ]

    retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=True)

def cmake_build():
    cmakeCmd = [
        'cmake', 
        '--build', build_options['build-dir'],
        '--config', build_options['config']
    ]
    retCode = subprocess.check_call(cmakeCmd, stderr=subprocess.STDOUT, shell=True)


def build():
    print('Starting build')
    set_build_directory()
    cmake_configure()
    cmake_build()
    pass

if __name__ == "__main__":
    print('---------------------------------------------------------------------')
    build()
    print('---------------------------------------------------------------------')