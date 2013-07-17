Name:		python-heatclient
Version:	0.2.3
Release:	1%{?dist}
Summary:	Python API and CLI for OpenStack Heat

Group:		Development/Languages
License:	ASL 2.0
URL:		http://pypi.python.org/pypi/python-heatclient
Source0:	http://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python-setuptools
BuildRequires:	python-d2to1
BuildRequires:	python-pbr

Requires:	python-argparse
Requires:	python-httplib2
Requires:	python-iso8601
Requires:	python-keystoneclient
Requires:	python-prettytable
Requires:	PyYAML

%description
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

%package doc
Summary:	Documentation for OpenStack Heat API Client
Group:		Documentation

BuildRequires:	python-sphinx

%description doc
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

This package contains auto-generated documentation.

%prep
%setup -q

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config.
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
echo "%{version}" > %{buildroot}%{python_sitelib}/heatclient/versioninfo

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files
%doc LICENSE README.rst
%{_bindir}/heat
%{python_sitelib}/heatclient
%{python_sitelib}/*.egg-info

%files doc
%doc html

%changelog
* Wed Jul 17 2013 Jakub Ruzicka <jruzicka@redhat.com> 0.2.3-1
- Updated to upstream version 0.2.3.
- Add new dependency: PyYAML.
- Add new build requires: python-d2to1 and python-pbr.
- Remove requirements.txt file.
- Generate versioninfo file.

* Mon Mar 11 2013 Steven Dake <sdake@redhat.com> 0.2.1-1
- copied from python-novaclient spec file and tailored to suit
