#!/usr/bin/env python

from distutils.core import setup

setup( name = "ansible-check",
       version = '0.9',
       description = 'Basic testing for ansible templates',
       url = 'https://github.com/javiplx/ansible-check',
       author = 'Javier Palacios',
       author_email = 'javiplx@gmail.com',
       packages = [ 'ansible_check' ],
       install_requires = [ 'ansible' ],
       scripts = [ 'bin/build_role' , 'bin/template_test' , 'bin/template_render' ]
    )

