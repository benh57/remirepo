# remirepo/fedora spec file for php-horde-Horde-Mongo
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Mongo
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Mongo
Version:        1.1.0
Release:        1%{?dist}
Summary:        Horde Mongo Configuration

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

# Fix autoloader path
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
%if 0%{?fedora} >= 21
Suggests:       php-pecl(mongo) >= 1.3.0
Suggests:       php-composer(alcaeus/mongo-php-adapter)
%endif

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-mongo) = %{version}


%description
Provides an API to ensure that the PECL Mongo extension can be used
consistently across various Horde packages.

Tu use this module, you also need to install
  - php-pecl-mongo (PHP 5 only)
or
  - php-pecl-mongodb (PHP 5 or 7)
  - php-alcaeus-mongo-php-adapter


%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml
%patch0 -p1 -b .rpm
sed -e '/Client.php/s/md5sum="[^"]*"//' \
    -e '/name="bundle/d' \
    -i %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


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
%dir %{pear_phpdir}/Horde
%{pear_phpdir}/Horde/Mongo


%changelog
* Wed Jul 13 2016 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0
- php-pecl-mongo and alcaeus/mongo-php-adapter are optional

* Sat Jul  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-4
- on switch to alcaeus/mongo-php-adapter with PHP >= 5.5

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 1.0.3-3
- drop dependency on mongo extension for PHP 7
- add dependency on alcaeus/mongo-php-adapter

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3
- add provides php-composer(horde/horde-mongo)

* Wed Oct 16 2013 Remi Collet <remi@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Fri Jun 14 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Wed Jun  5 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- update to 1.0.0

* Thu May 30 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.2.RC1
- update to 1.0.0RC1

* Mon May  6 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-0.1.beta1
- initial package
