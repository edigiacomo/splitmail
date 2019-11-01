Name:           splitmailbox
Version:        0.1
Release:        1%{?dist}
Summary:        Simple tool to split your mailbox or maildir.

License:        GPLv2+
URL:            https://github.com/edigiacomo/splitmailbox
Source0:        https://github.com/edigiacomo/splitmailbox/archive/v%{version}.tar.gz#%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
Requires:       python3

%description
Simple tool to split your mailbox or maildir.

%prep
%autosetup

%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%doc README.md
%{python3_sitelib}/%{name}-*.egg-info/
%{python3_sitelib}/%{name}/
%{_bindir}/splitmailbox


%changelog
* Fri Nov  1 2019 Emanuele Di Giacomo <emanuele@digiacomo.cc> - 0.1
- First release
