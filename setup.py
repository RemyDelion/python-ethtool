#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function

from distutils.core import setup, Extension
try:
    import commands
except ImportError:
    import subprocess as commands
import sys

version = '0.12'

def pkgconfig(pkg):
    def _str2list(pkgstr, onlystr):
        res = []
        for l in pkgstr.split(" "):
            if l.find(onlystr) == 0:
                res.append(l.replace(onlystr, "", 1))
        return res

    (res, cflags) = commands.getstatusoutput('pkg-config --cflags-only-other %s' % pkg)
    if res != 0:
        print('Failed to query pkg-config --cflags-only-other %s' % pkg)
        sys.exit(1)

    (res, includes) = commands.getstatusoutput('pkg-config --cflags-only-I %s' % pkg)
    if res != 0:
        print('Failed to query pkg-config --cflags-only-I %s' % pkg)
        sys.exit(1)

    (res, libs) = commands.getstatusoutput('pkg-config --libs-only-l %s' % pkg)
    if res != 0:
        print('Failed to query pkg-config --libs-only-l %s' % pkg)
        sys.exit(1)

    (res, libdirs) = commands.getstatusoutput('pkg-config --libs-only-L %s' % pkg)
    if res != 0:
        print('Failed to query pkg-config --libs-only-L %s' % pkg)
        sys.exit(1)


    # Clean up the results and return what we've extracted from pkg-config
    return {'cflags': cflags,
            'include': _str2list(includes, '-I'),
            'libs': _str2list(libs, '-l'),
            'libdirs': _str2list(libdirs, '-L')
            }


libnl = pkgconfig('libnl-3.0')
libnl['libs'].append('nl-route-3')

with open('README.rst') as f:
    long_description = f.read()

with open('CHANGES.rst') as f:
    long_description += '\n\n'
    long_description += f.read()

setup(name='ethtool',
      version=version,
      description='Python module to interface with ethtool',
      long_description=long_description,
      
      author='Harald Hoyer, Arnaldo Carvalho de Melo, David Sommerseth',
      author_email='davids@redhat.com',
      
      maintainer='Lumír Balhar, Miro Hrončok, Charalampos Stratakis, Sanqui',
      maintainer_email='python-maint@redhat.com',
      
      url='https://github.com/fedora-python/python-ethtool',
      license='GPL-2.0',
      keywords='network networking ethernet tool ethtool',

      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: POSIX :: Linux',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: System :: Networking',
      ],
      ext_modules=[
        Extension(
            'ethtool',
            sources = [
                'python-ethtool/ethtool.c',
                'python-ethtool/etherinfo.c',
                'python-ethtool/etherinfo_obj.c',
                'python-ethtool/netlink.c',
                'python-ethtool/netlink-address.c'],
            extra_compile_args=['-fno-strict-aliasing'],
            include_dirs = libnl['include'],
            library_dirs = libnl['libdirs'],
            libraries = libnl['libs'],
            define_macros = [('VERSION', '"%s"' % version)]
            )
        ]
)
