# remirepo/fedora spec file for php-horde-Horde-Autoloader
#
# Copyright (c) 2012-2017 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global bootstrap    0
%global pear_name    Horde_Autoloader
%global pear_channel pear.horde.org
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-horde-Horde-Autoloader
Version:        2.1.2
Release:        1%{?dist}
Summary:        Horde Autoloader

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

# Fedora specific - ensure Sabre is taken from /usr/share/php
# but Sabre\VObject from /usr/share/pear
Patch0:         %{name}-Sabre.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-autoloader) = %{version}


%description
Autoload implementation and class loading manager for Horde.


%prep
%setup -q -c

cd %{pear_name}-%{version}
%patch0 -p1 -b .fedora
sed -e '/Default.php/s/md5sum=".*" name/name/' \
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


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
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit .
fi
%else
: Test disabled, bootstrap build
%endif


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
%{pear_phpdir}/Horde/Autoloader
%{pear_phpdir}/Horde/Autoloader.php
%{pear_testdir}/%{pear_name}


%changelog
* Mon Feb 01 2016 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri Sep 25 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-3
- simplify ClassPathMapper patch for Sabre

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1
- add provides php-composer(horde/horde-autoloader)
- enable test during build

* Tue Mar 04 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Thu Feb 20 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-5
- new autoloader patch for SabreDAV and VObject

* Fri Jan  3 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- patch autoloader for Sabre

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Mon Nov  5 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- make test optional

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- rebuilt for new pear_testdir

* Sat Jun 16 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
