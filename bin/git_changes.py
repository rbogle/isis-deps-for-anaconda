#! /usr/bin/env python

import os
import argparse
import re
import sys
import logging
import subprocess

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Ojbect conversion of dict
class Config:
    # ref members as .
    def __init__(self, **entries):
        self.__dict__.update(entries)
    # make it iterable
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value

def git_isrepo(repo):
    repo="%s/.git" %repo
    if os.path.isdir(repo):
        log.debug("repo %s found" %repo )
        return True
    else:
        log.debug("repo %s not found" %repo)
        return False

def git_files_changed(repo='.',commit='HEAD'):
    if git_isrepo(repo):
        repo=repo="%s/.git" %repo
        str="git --git-dir %s diff-tree --no-commit-id --name-only -r" %repo
        cmd=str.split()
        cmd.append(commit)
        try:
            log.debug("Retrieving changed files")
            return subprocess.check_output(cmd).split()
        except subprocess.CalledProcessError as e:
            log.error("Call to git failed with %s" %e)
    return None

def match_regex(regexs, filelist):
    regex = "|".join(regexs)
    files = ",".join(filelist)
    if re.search(regex, files):
        return True
    return False

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--commit", help="refspec to check", default="HEAD")
    parser.add_argument("-r", "--regex", action='append', help="label to tag package with", default=argparse.SUPPRESS)
    parser.add_argument("-i", "--invert", help="invert search to 'not found'", action="store_true")
    parser.add_argument("repo", nargs="?", help="path to repo to examine", default=".")
    args = vars(parser.parse_args())
    
    config = {
        "base_path": os.getcwd(),
        "commit": args.get("commit", "HEAD"),
        "repo": args.get('repo', '.'),
        "regex": args.get('regex', ['.*']),
        "invert": args.get('invert')
    }
    return Config(**config)

if __name__ == '__main__':

    conf = parse_args()

    files = git_files_changed(conf.repo,conf.commit)
    match = match_regex(conf.regex,files)

    filelist= "\n".join(files)
    if not match:
        sys.exit("Watched files were not changed: \n%s" %filelist)
    
    print("Watchted files were changed: \n%s" %filelist)
    