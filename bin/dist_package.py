#! /usr/bin/env python

import os
import argparse
import json
import sys
import glob
import platform
import subprocess

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

def anaconda_logout():
    cmd = ["anaconda", "logout"]
    try:
        print("Trying logout from anaconda.org")
        subprocess.call(cmd)
    except subprocess.CalledProcessError:
        print("logout from anaconda.org failed")
        raise

def anaconda_login(user,passwd):
    cmd = ["anaconda", "login"]
    cmd.extend(["--username", user])
    cmd.extend(["--password", passwd])
    try:
        print("Trying login to anaconda.org")
        subprocess.call(cmd)
    except subprocess.CalledProcessError:
        print("Login to anaconda.org failed")
        raise

def anaconda_upload(file,user=None,labels=None,token=None,force=False):

    cmd = ['anaconda']
    if token:
        cmd.extend(["--token", token])
    cmd.append("upload")
    if force:
        cmd.append("--force")
    if user:
        cmd.extend(["--user", user])
    if labels:
        for l in labels:
            cmd.extend(["-l", l])
    cmd.append(file)
    try:
        print("Attempting Upload of %s to anaconda.org" %file )
        print("cmd is %s" %cmd)
        subprocess.call(cmd)
    except subprocess.CalledProcessError:
        print("Upload of %s to anaconda.org failed" %file)
        raise

def process_log(config):
    try:
        log = json.load(open(config.get('log')))
        for platform,packages in log.iteritems():
            for package in packages:
                if package["artifact"]:
                    try:
                        anaconda_upload(package['artifact'], config.get("user"), config.get('labels'), config.get('token'), config.get('force'))
                    except:
                        print "upload of %s to anaconda failed." %pkg
    except:
        sys.exit( "invalid log file: %s could not be found or parsed" %config.get("log"))


def process_list(config):
    if not config.get('token'):
        try:
            anaconda_logout()
            anaconda_login(config.get("user"), config.get("passwd"))
        except:
            sys.exit("could not login in with credentials provided...")
    for pkg_name in config.get("packages"):
        path = "%s/%s/%s" %(config.get('src_path'),config.get('platform'),pkg_name)
        files = glob.glob(path+'*.tar.bz2')
        for pkg in files:
            try:
                anaconda_upload(pkg, config.get("user"), config.get('labels'), config.get('token'), config.get('force'))
            except:
                print "upload of %s to anaconda failed." %pkg

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="path to the build log file", default=argparse.SUPPRESS)
    parser.add_argument("-s", "--src", help="src path for the built pkgs", default=argparse.SUPPRESS)
    parser.add_argument("-u", "--user", help="user to upload to in anaconda cloud", default=argparse.SUPPRESS)
    parser.add_argument("-t", "--token", help="token for uploading", default=argparse.SUPPRESS)
    parser.add_argument("-l", "--label", action='append', help="label to tag package with", default=argparse.SUPPRESS)
    parser.add_argument("-p", "--passwd", help="password for uploading", default=argparse.SUPPRESS)   
    parser.add_argument("--force", help="force package overwrite on server", action="store_true")
    parser.add_argument("packages", nargs='*', help="which package(s) to process, specifying 'all' will process all found")
    args = vars(parser.parse_args())
    
    config = {
        "base_path": os.getcwd(),
        "src_path": args.get('src', '%s/build' %os.getcwd()),
        "labels": args.get('label', list()),
        "log": args.get('file', None),
        "user": args.get('user', "usgs-astrogeology"),
        "passwd": args.get('passwd', None),
        "token": args.get('token', None),
        "platform": get_plaformid(),
        "force": args.get("force"),
        'packages': args['packages']
    }
    return config

if __name__ == '__main__':

    config = parse_args()

    if config.get('log'):
        process_log(config) 
    else:
        process_list(config)