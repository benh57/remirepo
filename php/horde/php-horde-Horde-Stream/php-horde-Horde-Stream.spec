# remirepo/fedora spec file for php-horde-Horde-Stream
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Stream
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Stream
Version:        1.6.3
Release:        1%{?dist}
Summary:        Horde stream handler

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml, required
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
# From package.xml, optional
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# From phpcompatinfo report for version 1.6.0
Requires:       php-json

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
An object-oriented interface to assist in creating and storing PHP stream
resources, and to provide utility methods to access and manipulate the
stream contents.


%prep
%setup -q -c
cd %{pear_name}-%{version}
cp ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit .
fi


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Stream
%{pear_phpdir}/Horde/Stream.php
%{pear_testdir}/%{pear_name}


%changelog
* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.6.3-1
- Update to 1.6.3
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 1.6.2-1
- Update to 1.6.2

* Wed Feb 12 2014 Remi Collet <remi@fedoraproject.org> - 1.6.1-1
- Update to 1.6.1
- add optional dependencies, Horde_Stream_Wrapper, Horde_Util

* Wed Feb 12 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Tue Nov 12 2013 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Tue Oct 15 2013 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0

* Mon Aug 05 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0 for remi repo

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 for remi repo

* Sat Nov  3 2012 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- Initial package

