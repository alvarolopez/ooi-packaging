FROM centos:7

RUN yum install -y epel-release rpm-build git python-setuptools
RUN yum install -y epel-rpm-macros python-pbr

RUN mkdir -p /root/rpmbuild/RPMS \
             /root/rpmbuild/SOURCES \
             /root/rpmbuild/SPECS \
             /root/rpmbuild/SRPMS \
             /root/rpmbuild/BUILD \
             /root/rpmbuild/BUILDROOT

COPY rpmbuild.sh /root
RUN  chmod +x /root/rpmbuild.sh

CMD  /root/rpmbuild.sh
