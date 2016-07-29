#!/bin/bash

set -e

# Expects $1 to be the version to build
if [ "x$1" = "x" ]; then
    echo "Expecting version number as argument"
    exit 1 
fi

git clone https://git.openstack.org/openstack/ooi /tmp/ooi

pushd /tmp/ooi
git checkout $1
python setup.py sdist
cp dist/ooi-$1.tar.gz /root/rpmbuild/SOURCES/ 
popd 

rpmbuild -ba /root/rpmbuild/SPECS/ooi.spec
