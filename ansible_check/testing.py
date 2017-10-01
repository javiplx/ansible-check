
from jinja2 import Template

from ansible.utils import merge_hash

import yaml
import os

from codecs import open

def read_file( file_name ) :
    output = ""
    with open( file_name , encoding='utf-8' ) as fd :
        for line in fd.readlines() :
            output += line
    return output


def get_deps( dependencies , rolename=None ) :
    newdeps = []
    if rolename :
        meta_file = os.path.normpath( os.path.join( os.sys.argv[1] , '..' , rolename , "meta/main.yml" ) )
    else :
        meta_file = os.path.normpath( os.path.join( os.sys.argv[1] , "meta/main.yml" ) )
    if os.path.isfile( meta_file ) :
        meta = yaml.load( open( meta_file ) )
        for dep in meta.get('dependencies',()) :
            if isinstance(dep, dict) :
                if dep['role'] not in dependencies + newdeps :
                    newdeps.append( dep['role'] )
            else :
                if dep not in dependencies + newdeps :
                  newdeps.append( dep )
    dependencies.extend( newdeps )
    for dep in newdeps :
        get_deps( dependencies , dep )
    return dependencies

def add_vars ( invars , template , runtime ) :
    return merge_hash( invars , yaml.load( template.render(runtime) ) )


def defaults( env , runtime , vars_file=None ) :

    if vars_file :
        extra_vars = yaml.load( open( vars_file ) )
        runtime.update(extra_vars)

    defaults = {
      'django': {},
      'groups': {},
      'ansible_eth0': {
        'ipv4': {
          'address':'127.0.0.1'
          }
        }
      }

    for dep in get_deps([]) :
        meta_file = os.path.normpath( os.path.join( os.sys.argv[1] , '..' , dep , 'defaults/main.yml' ) )
        if os.path.isfile( meta_file ) :
            defaults = add_vars( defaults , Template( read_file( meta_file ) ) , runtime )

    defaults = add_vars( defaults , env.get_template('defaults/main.yml') , runtime )
    if os.path.isfile( os.path.join( os.sys.argv[1] , 'vars/main.yml' ) ) :
        defaults = add_vars( defaults , env.get_template('vars/main.yml') , runtime )

    return merge_hash( defaults , runtime )

