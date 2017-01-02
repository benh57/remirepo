# remirepo/fedora spec file for php-horde-Horde-Mime-Viewer
#
# Copyright (c) 2012-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Mime_Viewer
%global pear_channel pear.horde.org
# To use system js
%global with_sysjs   0
# no test for now (all skipped)
%global with_tests   0%{?_with_tests:1}

Name:           php-horde-Horde-Mime-Viewer
Version:        2.2.1
Release:        1%{?dist}
Summary:        Horde MIME Viewer Library

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
%if %{with_sysjs}
Requires:       syntaxhighlighter
%else
Provides:       horde-syntaxhighlighter
%endif
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-dom
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xsl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Compress) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
# Optional
Requires:       php-pear(Net_DNS2)

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-mime-viewer) = %{version}


%description
Provides rendering drivers for MIME data.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Don't install syntaxhighlighter, use system one
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
%if %{with_sysjs}
    -e '/syntaxhighlighter/d' \
%endif
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
rm -rf %{buildroot}
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
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%clean
rm -rf %{buildroot}


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose .
# remirepo:2
fi
exit $ret
%else
: Test disabled, missing '--with tests' option.
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Mime/Viewer
%{pear_phpdir}/Horde/Mime/Viewer.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%if ! %{with_sysjs}
%{pear_hordedir}/js/syntaxhighlighter
%endif


%changelog
* Wed Sep 07 2016 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Thu Jul 28 2016 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2
- PHP 7 compatible version

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- add optional dependency on Net_DNS2
- add provides php-composer(horde/horde-mime-viewer)

* Tue Nov 18 2014 Remi Collet <remi@fedoraproject.org> - 2.0.8-1
- Update to 2.0.8
- raise dependency on Horde_Translation 2.2.0

* Tue Sep 23 2014 Remi Collet <remi@fedoraproject.org> - 2.0.7-2
- don't use system syntaxhighlighter as this breaks horde
  and its cache system

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 2.0.7-1
- Update to 2.0.7

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 2.0.6-1
- Update to 2.0.6

* Fri Jan 10 2014 Remi Collet <remi@fedoraproject.org> - 2.2.1-2
- cleanups from review #895622

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5
- switch from Conflicts >= max to Requires < max

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 for remi repo

* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-3
- use Alias for system JS

* Tue Jan 15 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-2
- use system syntaxhighlighter

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 for remi repo
- use local script instead of find_lang

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1 for remi repo

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Initial package
