#
# ooi RPM
#

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Summary     : OpenStack OCCI Interface
Name        : python-ooi
Version     : 0.3.1
Release     : 1%{?dist}
Group       : Applications/Internet
License     : ASL 2.0
URL         : https://launchpad.net/ooi
Source      : ooi-%{version}.tar.gz

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: python-setuptools
BuildRequires: python-pbr
Requires: python
Requires: python-oslo-config
Requires: python-oslo-log
Requires: python-routes
Requires: python-six
Requires: python-webob

%description
ooi is an implementation of the Open Cloud Computing Interface (OCCI) for
OpenStack.

%prep
%setup -q -n ooi-%{version}

%build

%install
rm -rf $RPM_BUILD_ROOT
python setup.py install --root $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{python_sitelib}/ooi*

%changelog
* Wed Jul 20 2016 Enol Fernandez <enol.fernandez@egi.eu> 0.3.1
- Modify structure of test to separe functional tests
- Move neutron_ooi_endpoint to nova.conf
- Merge "Delete extra parameter in network link creation"
- Merge "Solved OCCI validation using osnetwork mixin"
- gitbook: point to online documentation
- doc: link to usage instructions in index
- doc: include packages information
- Include storage documentation in usage
- Update documentation and gitbook
- Delete extra parameter in network link creation
- Solved OCCI validation using osnetwork mixin
- tests: separate between functional and unit
- Merge "Add functional tests for network"
- Add copyright as required in INDIGO-DataCloud
- Add functional tests for network
* Wed Jun 15 2016 Enol Fernandez <enol.fernandez@egi.eu> 0.3.0
- Support for neutron networking
* Mon Mar 21 2016 Enol Fernandez <enol.fernandez@egi.eu> 0.2.0
- Initial RPM version
