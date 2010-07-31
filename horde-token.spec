%define prj     Horde_Token

%define xmldir  %{_var}/lib/pear
%define peardir %(pear config-get php_dir 2> /dev/null)

Name:		horde-token
Version:	0.0.4
Release:	%mkrel 2
Summary:	Horde Token API
License:	LGPL
Group:		Networking/Mail
Url:		http://pear.horde.org/index.php?package=%{prj}
Source0:	%{prj}-%{version}.tgz
BuildArch:	noarch
Requires(pre):  php-pear
Requires:	horde-util
BuildRequires:	php-pear
BuildRequires:	php-pear-channel-horde

%description
The Horde_Token:: class provides a common abstracted interface into the
various token generation mediums. It also includes all of the functions
for retrieving, storing, and checking tokens.

%prep
%setup -q -n %{prj}-%{version}

%build
%__mv ../package.xml .

%install
pear install --packagingroot %{buildroot} --nodeps package.xml

%__rm -rf %{buildroot}/%{peardir}/.{filemap,lock,registry,channels,depdb,depdblock}

%__mkdir_p %{buildroot}%{xmldir}
%__cp package.xml %{buildroot}%{xmldir}/%{prj}.xml

%clean
%__rm -rf %{buildroot}

%post
# For unknown reason the package horde-util fails with this error message:
# installing horde-token-0.0.4-5.1
# Package "/var/lib/pear/Horde_Token.xml" is not valid
# install failed
# error: %post(horde-token-0.0.4-5.1.noarch) scriptlet failed, exit status 1
# mount: can't find / in /etc/fstab or /etc/mtab
# System halted.
# =======================
# For this reason include the || echo > /dev/null to prevent the horde-util
# build to bark out of the build process
pear install --nodeps --soft --force --register-only %{xmldir}/%{prj}.xml || echo > /dev/null

%postun
if [ "$1" -eq "0" ]; then
  pear uninstall --nodeps --ignore-errors --register-only pear.horde.org/%{prj}
fi

%files
%defattr(-, root, root)
%{xmldir}/%{prj}.xml
%dir %{peardir}/Horde
%dir %{peardir}/Horde/Token
%{peardir}/Horde/Token.php
%{peardir}/Horde/Token/file.php
%{peardir}/Horde/Token/sql.php

