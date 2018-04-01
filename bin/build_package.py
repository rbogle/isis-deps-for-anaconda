#! /usr/bin/env python

import yaml
import os
import argparse
import platform
import json
import sys
from jinja2 import Environment, FileSystemLoader
from conda_build import api as conda
from time import gmtime,strftime

def load_config(filename):
    with open(filename, 'r') as f:
        config = yaml.load(f)
        return config

def get_all_pkgs(recipe_root):
    packages=list()
    for package in os.listdir(recipe_root):
        packages.append(package)
    packages.sort()
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

def get_plaformid():
    p = platform.machine()
    s = platform.system()
    if s == "Darwin":
        s = "osx"
    if s == 'Linux':
        s = 'linux'
    if p == "x86_64":
        p ="-64"
    return "%s%s" %(s,p)


def write_bld_log(logname, log):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    logname="./logs/%s" %(logname)
    with open(logname, 'w') as f:
        f.write(json.dumps(log, indent=4, sort_keys=True))
        return True
    return False

def add_bldlog_entry(log, package, result, upload, err):
    id = get_plaformid()
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    msgs = log.get(id, list())
    msg = {
        'timestamp': time,
        'package': package,
        'artifact': result,
        'upload': upload,
        'err': err
    }
    msgs.append(msg)
    if not log.get(id):
        log[id]=msgs

def build_pkg(recipe_path, outputdir, config, log):
    build_config={
        'output_folder': outputdir,
        'python': config.get('python', '2.7'),
        'numpy': config.get('numpy', '1.11'),
        'channels': config.get('channel'),
        'verbose' : not config.get('quiet')
    }
    upload=False; status = True; err=""; result=""; package=""
    # if noupload is true turn off,  default is to upload
    # conda.build only check for user or token being set. 
    if not config['noupload']:
        upload = True
        build_config['user']= config.get('user')
        build_config["token"]=config.get('token')

    try:
        result = conda.build(recipe_path, **build_config)
    except Exception as e :
        err = "build of %s failed. Error is %s" %(recipe_path,e)
        status = False

    if result :
        package = os.path.relpath(result[0])


    add_bldlog_entry(log,config['build_pkg'],package, upload, err)
    return status

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
    parser.add_argument("-t", "--token", help="token for uploading", default=argparse.SUPPRESS)
    parser.add_argument("-q", "--quiet", help="suppress messages", action="store_true")
    parser.add_argument("--buildlog", help="name for buildlog", default=argparse.SUPPRESS)
    parser.add_argument("--hardfail", help="fail on individual package build failure", action="store_true")
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
    hardfail = args.get("hardfail")
    build_logname = args.get('buildlog', '%s-%s.log' %(get_plaformid(),strftime("%Y%m%d_%H%M%S", gmtime())))
  
    packages=args['packages']
    if ('all' in packages):
        packages = get_all_pkgs(recipies_path)
    elif not packages:
        parser.print_help(sys.stderr)
        sys.exit(1)

    print "Operating on packages: {}".format(' '.join(packages))

    config = load_config(config_file)
    config['channel'] = channel
    config['user'] = args.get('user', 'usgs-astrogeology')
    config['token'] = args.get('token', None)
    config['noupload'] = args.get('noupload')
    config['quiet'] = args.get('quiet')

    build_log={}

    for package in packages:

        recipe_meta_tmpl = '%s/%s/meta.yaml.tmpl' %(recipies_path,package)
        recipe_meta = '%s/%s/meta.yaml' %(recipies_path,package)
        recipe_path = '%s/%s' %(recipies_path,package)
        config['build_pkg'] = package
        success=True
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
            success=build_pkg(recipe_path, dest_path, config, build_log)
        else:
            print "Skipping build of %s ..." %package
            success=False
            add_bldlog_entry(build_log,config['build_pkg'],"", False, "No build option selected")

        if hardfail and not success:
            write_bld_log(build_logname,build_log)
            sys.exit("Package %s failed to build, exiting" %package)

    write_bld_log(build_logname,build_log)
