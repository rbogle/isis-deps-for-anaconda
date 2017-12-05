#! /usr/bin/env python

import yaml
import os
import argparse
from jinja2 import Environment, FileSystemLoader
from conda_build import api as conda

def load_config(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f)
        return config

def get_all_pkgs(recipe_root):
    packages=list()
    for package in os.listdir(recipe_root):
        packages.append(package)
    return packages

def render_tmpl(templatepath, config):
    path,filename = os.path.split(templatepath)
    return Environment(loader=FileSystemLoader(path or './')).get_template(filename).render(config)

def write_meta(meta_inp, meta_outp, config):

    if os.path.isfile(recipe_meta_tmpl):
        with open(meta_outp, 'w') as f:
            meta = render_tmpl(meta_inp, config)
            f.write(meta)
            return True
    return False

def build_pkg(recipe_path, outputdir, config):
    build_config={
        'output_folder': outputdir,
        'python': config.get('python', '2.7'),
        'numpy': config.get('numpy', '1.11'),
        'channels': config.get('channel'),

    }
    # if noupload is true turn off default is to upload
    if not config['noupload']:
        build_config['user']= config.get('user')

    try:
        conda.build(recipe_path, **build_config)
    except Exception as e :
        print "build of %s failed." %recipe_path
        print e

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--config", help="path to the config file", default=argparse.SUPPRESS)
    parser.add_argument("-r", "--recipies", help="path where recipes live",default=argparse.SUPPRESS)
    parser.add_argument("-d", "--dest", help="destination path for the build", default=argparse.SUPPRESS)
    parser.add_argument("-c", "--channel", nargs='*', help="additional channels to use in build", default=argparse.SUPPRESS)
    parser.add_argument("-n", "--nometa", help="do not generate new meta.yaml from template", action="store_true")
    parser.add_argument("-b", "--nobuild", help="do not build the packages", action="store_true")
    parser.add_argument("-y", "--noprompt", help="do not prompt for input on each package", action="store_true")
    parser.add_argument("-l", "--noupload", help="upload files after build", action="store_true")
    parser.add_argument("-u", "--user", help="user to upload to in anaconda cloud", default=argparse.SUPPRESS)
    parser.add_argument("packages", nargs='*', help="which package(s) to process, specifying 'all' will process all found")
    args = vars(parser.parse_args())

    base_path = os.getcwd()
    config_file = args.get('config', '%s/meta/conda_build_config.yaml' %base_path)
    recipies_path = args.get('recipies', '%s/recipies' %base_path)
    dest_path = args.get('dest', '%s/build' %base_path)
    channel=args.get('channel', list())
    no_meta = args.get('nometa')
    no_prompt = args.get('noprompt')
    no_build = args.get('nobuild')

    packages=args['packages']
    if ('all' in packages):
        packages = get_all_pkgs(recipies_path)

    print "Operating on packages: {}".format(' '.join(packages))

    config = load_config(config_file)
    config['channel'] = channel
    config['user'] = args.get('user', 'usgs-astrogeology')
    config['noupload'] = args.get('noupload')

    for package in packages:

        recipe_meta_tmpl = '%s/%s/meta.yaml.tmpl' %(recipies_path,package)
        recipe_meta = '%s/%s/meta.yaml' %(recipies_path,package)
        recipe_path = '%s/%s' %(recipies_path,package)

        if not no_prompt:
            res=raw_input('Do you want to process %s (y/n)? ' %package)
            if res is not 'y':
                continue

        if not no_meta:
            print "Generating meta file from template for package %s" %package
            if not write_meta(recipe_meta_tmpl,recipe_meta,config):
                print "No template found for %s" %package
            else:
                print "New meta.yaml generated for %s" %package
        else:
            print "Will use existing meta file for %s" %package
        if not no_build:
            build_pkg(recipe_path, dest_path, config)
        else:
            print "Skipping build of %s ..." %package
