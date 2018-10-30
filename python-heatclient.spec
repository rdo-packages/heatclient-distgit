# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname heatclient

%global common_desc \
This is a client for the OpenStack Heat API. There's a Python API (the \
heatclient module), and a command-line script (heat). Each implements 100% of \
the OpenStack Heat API.

Name:    python-heatclient
Version: XXX
Release: XXX
Summary: Python API and CLI for OpenStack Heat

License: ASL 2.0
URL:     https://launchpad.net/python-heatclient
Source0: https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch: noarch

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary: Python API and CLI for OpenStack Heat
%{?python_provide:%python_provide python%{pyver}-heatclient}
%if %{pyver} == 3
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires: python%{pyver}-devel
BuildRequires: python%{pyver}-setuptools
BuildRequires: python%{pyver}-pbr
BuildRequires: git

Requires: python%{pyver}-babel
Requires: python%{pyver}-iso8601
Requires: python%{pyver}-keystoneauth1 >= 3.4.0
Requires: python%{pyver}-osc-lib >= 1.8.0
Requires: python%{pyver}-prettytable
Requires: python%{pyver}-pbr
Requires: python%{pyver}-six
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-oslo-i18n >= 3.15.3
Requires: python%{pyver}-swiftclient >= 3.2.0
Requires: python%{pyver}-requests
Requires: python%{pyver}-cliff
# Handle python2 exception
%if %{pyver} == 2
Requires: PyYAML
%else
Requires: python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}

%package doc
Summary: Documentation for OpenStack Heat API Client

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-openstackdocstheme
BuildRequires: python%{pyver}-babel
BuildRequires: python%{pyver}-iso8601
BuildRequires: python%{pyver}-keystoneauth1
BuildRequires: python%{pyver}-osc-lib
BuildRequires: python%{pyver}-prettytable
BuildRequires: python%{pyver}-pbr
BuildRequires: python%{pyver}-six
BuildRequires: python%{pyver}-oslo-serialization
BuildRequires: python%{pyver}-oslo-utils
BuildRequires: python%{pyver}-oslo-i18n
BuildRequires: python%{pyver}-swiftclient
BuildRequires: python%{pyver}-requests
BuildRequires: python%{pyver}-cliff

%description doc
%{common_desc}

This package contains auto-generated documentation.

%prep
%autosetup -n %{name}-%{upstream_version} -S git

rm -rf {test-,}requirements.txt tools/{pip,test}-requires


%build
%{pyver_build}

%install
%{pyver_install}
echo "%{version}" > %{buildroot}%{pyver_sitelib}/heatclient/versioninfo
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s heat %{buildroot}%{_bindir}/heat-%{pyver}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/heat.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/heat

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/heatclient/tests


export PYTHONPATH=.
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# generate man page
sphinx-build-%{pyver} -W -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/heat.1 %{buildroot}%{_mandir}/man1/heat.1

%files -n python%{pyver}-%{sname}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/heatclient
%{pyver_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%{_mandir}/man1/heat.1.gz
%{_bindir}/heat
%{_bindir}/heat-%{pyver}

%files doc
%doc doc/build/html
%license LICENSE

%changelog
