# ooi-packaging

Build the docker container
```
docker build -t ooirpm .
```


Check the spec is ok, update the changelog (e.g. from 0.3.0 to 0.3.1):
```
git log 0.3.0..0.3.1 --oneline
```

Build the rpm, e.g. for 0.3.1:
```
docker run --rm -it -v $PWD/spec:/root/rpmbuild/SPECS -v $PWD/rpms:/root/rpmbuild/RPMS ooirpm /root/rpmbuild.sh 0.3.1
```

Results will be at `$PWD/rpms`
