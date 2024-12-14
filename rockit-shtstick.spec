Name:      rockit-shtstick
Version:   %{_version}
Release:   1
Summary:   Internal temperature and humidity
Url:       https://github.com/rockit-astro/shtstickd
License:   GPL-3.0
BuildArch: noarch

%description


%build
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}/etc/bash_completion.d
mkdir -p %{buildroot}%{_sysconfdir}/shtstickd/
mkdir -p %{buildroot}%{_udevrulesdir}

%{__install} %{_sourcedir}/shtstick %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/shtstickd %{buildroot}%{_bindir}
%{__install} %{_sourcedir}/shtstickd@.service %{buildroot}%{_unitdir}
%{__install} %{_sourcedir}/completion/shtstick %{buildroot}/etc/bash_completion.d/shtstick

%package server
Summary:  Sensor server
Group:    Unspecified
Requires: python3-rockit-shtstick
%description server

%package client
Summary:  Sensor client
Group:    Unspecified
Requires: python3-rockit-shtstick
%description client

%files server
%defattr(0755,root,root,-)
%{_bindir}/shtstickd
%defattr(0644,root,root,-)
%{_unitdir}/shtstickd@.service

%files client
%defattr(0755,root,root,-)
%{_bindir}/shtstick
/etc/bash_completion.d/shtstick

%changelog
