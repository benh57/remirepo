# remirepo/fedora spec file for php-horde-Horde-Auth
#
# Copyright (c) 2012-2017 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Auth
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Auth
Version:        2.2.1
Release:        1%{?dist}
Summary:        Horde Authentication API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Db) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-ctype
Requires:       php-date
Requires:       php-ftp
Requires:       php-hash
Requires:       php-ldap
Requires:       php-pcre
Requires:       php-pdo
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Db) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_History) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imsp) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imsp) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Ldap) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Ldap) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Lock) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
# optional and not required for circular dep: Horde_Kolab_Session

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-auth) = %{version}


%description
The Horde_Auth package provides a common interface into the various
backends for the Horde authentication system.


%prep
%setup -q -c

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d $loc && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:)

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || : ignore
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
# hex2bin is 5.4 only
if php -r 'exit(function_exists("hex2bin") ? 0 : 1);'
then %{_bindir}/phpunit .
else : test ignored
fi
# remirepo:2
fi
exit $ret


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Auth
%{pear_phpdir}/Horde/Auth.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration


%changelog
* Sun Dec 04 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 2.1.12-1
- Update to 2.1.12

* Mon Feb 01 2016 Remi Collet <remi@fedoraproject.org> - 2.1.11-1
- Update to 2.1.11
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Tue Jul 07 2015 Remi Collet <remi@fedoraproject.org> - 2.1.10-1
- Update to 2.1.10

* Mon Jun 29 2015 Remi Collet <remi@fedoraproject.org> - 2.1.9-1
- Update to 2.1.9

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.1.8-1
- Update to 2.1.8

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 2.1.7-1
- Update to 2.1.7

* Fri Jan  9 2015 Remi Collet <remi@fedoraproject.org> - 2.1.6-1.1
- add upstream patch for blowfish test

* Thu Jan 08 2015 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- Update to 2.1.6
- add provides php-composer(horde/horde-auth)
- add dependency on Horde_Translation 2.2.0

* Tue Jun 17 2014 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Tue Mar 04 2014 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Tue Oct 15 2013 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Jan 29 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.3-1
- Update to 2.0.3 for remi repo

* Wed Jan  9 2013 Remi Collet <RPMS@FamilleCollet.com> - 2.0.2-1
- Update to 2.0.2 for remi repo
- use local script instead of find_lang

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Update to 2.0.1 for remi repo

* Fri Nov  2 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-2
- run test during build

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.4.9-1
- Upgrade to 1.4.9

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.4.7-1
- Initial package
