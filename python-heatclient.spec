%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname heatclient

%if 0%{?fedora}
%global with_python3 1
%endif

Name:    python-heatclient
Version: XXX
Release: XXX
Summary: Python API and CLI for OpenStack Heat

License: ASL 2.0
URL:     https://launchpad.net/python-heatclientclient
Source0: https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch: noarch

%description
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

%package -n python2-%{sname}
Summary: Python API and CLI for OpenStack Heat
%{?python_provide:%python_provide python2-heatclient}
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-pbr

Requires: python-babel
Requires: python-cliff
Requires: python-iso8601
Requires: python-keystoneauth1 >= 2.18.0
Requires: python-osc-lib >= 1.2.0
Requires: python-prettytable
Requires: python-pbr
Requires: python-six
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-utils >= 3.18.0
Requires: python-oslo-i18n >= 2.1.0
Requires: python-swiftclient >= 3.2.0
Requires: python-requests
Requires: PyYAML

%description -n python2-%{sname}
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

%if 0%{?with_python3}
%package -n python3-%{sname}
Summary: Python API and CLI for OpenStack Heat
%{?python_provide:%python_provide python3-heatclient}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pbr

Requires: python3-babel
Requires: python3-cliff
Requires: python3-iso8601
Requires: python3-keystoneauth1 >= 2.18.0
Requires: python3-osc-lib >= 1.2.0
Requires: python3-prettytable
Requires: python3-pbr
Requires: python3-six
Requires: python3-oslo-serialization >= 1.10.0
Requires: python3-oslo-utils >= 3.18.0
Requires: python3-oslo-i18n >= 2.1.0
Requires: python3-swiftclient >= 3.2.0
Requires: python3-requests
Requires: python3-PyYAML

%description -n python3-%{sname}
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.
%endif

%package doc
Summary: Documentation for OpenStack Heat API Client

BuildRequires: python-sphinx
BuildRequires: python-oslo-sphinx

%description doc
This is a client for the OpenStack Heat API. There's a Python API (the
heatclient module), and a command-line script (heat). Each implements 100% of
the OpenStack Heat API.

This package contains auto-generated documentation.

%prep
%setup -q -n %{name}-%{upstream_version}

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
echo "%{version}" > %{buildroot}%{python3_sitelib}/heatclient/versioninfo
mv %{buildroot}%{_bindir}/heat %{buildroot}%{_bindir}/heat-%{python3_version}
ln -s ./heat-%{python3_version} %{buildroot}%{_bindir}/heat-3
# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/heatclient/tests
%endif

%py2_install
echo "%{version}" > %{buildroot}%{python2_sitelib}/heatclient/versioninfo
mv %{buildroot}%{_bindir}/heat %{buildroot}%{_bindir}/heat-%{python2_version}
ln -s ./heat-%{python2_version} %{buildroot}%{_bindir}/heat-2

ln -s ./heat-2 %{buildroot}%{_bindir}/heat

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/heat.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/heat

# Delete tests
rm -fr %{buildroot}%{python2_sitelib}/heatclient/tests


export PYTHONPATH="$( pwd ):$PYTHONPATH"
sphinx-build -b html doc/source html

# generate man page
sphinx-build -b man doc/source man
install -p -D -m 644 man/heat.1 %{buildroot}%{_mandir}/man1/heat.1

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%files -n python2-%{sname}
%doc README.rst
%license LICENSE
%{python2_sitelib}/heatclient
%{python2_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/heat.1.gz
%{_bindir}/heat
%{_bindir}/heat-2
%{_bindir}/heat-%{python2_version}

%if 0%{?with_python3}
%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/heat.1.gz
%{_bindir}/heat-3
%{_bindir}/heat-%{python3_version}
%endif

%files doc
%doc html
%license LICENSE

%changelog
# REMOVEME: error caused by commit http://git.openstack.org/cgit/openstack/python-heatclient/commit/?id=5da87fc6d49ea5a70096f856cefe40dc3a9d9f0e
