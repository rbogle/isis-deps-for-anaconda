#!/usr/bin/env python

import yaml
import os
import os.path

recipe_root="./recipies"
build_deps = dict()
run_deps = dict()

for package in os.listdir(recipe_root):

    filename="%s/%s/meta.yaml.rendered" %(recipe_root,package)
    if not os.path.isfile(filename):
        filename="%s/%s/meta.yaml" %(recipe_root,package)
    with open(filename, 'r') as f:
        doc = yaml.load(f)
        name = doc.get('package').get('name')
        version = doc.get('package').get('name')
        build_reqs = doc.get("requirements", dict()).get("build",list())
        run_reqs = doc.get("requirements", dict()).get("run", list())
        for depstr in build_reqs:
            dep=depstr.split()
            if dep[0] not in build_deps:
                build_deps[dep[0]]=list()
            spec={'pkgname': name}
            if len(dep)>=2:
                spec['requires'] =dep[1]
            build_deps[dep[0]].append(spec)
        for runstr in run_reqs:
            dep=runstr.split()
            if dep[0] not in run_deps:
                run_deps[dep[0]]=list()
            spec={'pkgname': name}
            if len(dep)>=2:
                spec['requires'] =dep[1]
            run_deps[dep[0]].append(spec)
output={ "Build-Deps": build_deps, "Run-Deps": run_deps}
print yaml.dump(output)
