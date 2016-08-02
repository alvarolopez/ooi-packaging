I normally build like this.

First prepare the release

    cd original-git-repo
    git tag -s ...
    python setup.py sdist
    cd ../packaging-repo
    gbp import-orig ../original-git-repo/dist/whatever-1.2.3.tar.gz


Now elaborate the changelog

    git checkout upstream-git
    git pull (remote repo)
    git merge master
    gbp dch --release --commit
    # Do whatever changes are needed in debian control files (dependencies, etc)

Then, cherry pick the changelog commit (and any other to the debian control files)

    git checkout debian
    git cherry-pick ...

Lastly before building, cherry pick the commits again into the master one

    git checkout master
    git cherry-pick ...

And now, build the package:

    gbp buildpackage --git-verbose --git-export-dir=/tmp/output --git-tag
