# remirepo/fedora spec file for php-pear-phing
#
# Copyright (c) 2013-2016 Remi Collet
# Copyright (c) 2010-2013 Christof Damian
# Copyright (c) 2007-2010 Alexander Kahl
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    phing
%global pear_channel pear.phing.info

Summary:       A project build system based on Apache Ant
Name:          php-pear-phing
Version:       2.15.1
Release:       1%{?dist}

License:       LGPLv2
Group:         Development/Tools
URL:           http://phing.info/trac/

# remove non-free stuff
# pear download phing/phing
# ./strip.sh %{version}
Source0:       %{pear_name}-%{version}-strip.tgz
Source1:       strip.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires: php(language) >= 5.2.0
BuildRequires: php-pear(PEAR) >= 1.8.0
BuildRequires: php-channel(%{pear_channel})
BuildRequires: dos2unix

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:      php-cli
# From package.xml, Required
Requires:      php(language) >= 5.2.0
Requires:      php-pear(PEAR) >= 1.8.0
Requires:      php-channel(%{pear_channel})
# From package.xml, Optional
Requires:      php-pear(pear.phpunit.de/PHP_CodeCoverage) >= 1.1.0
Requires:      php-pear(pear.phpunit.de/phploc) >= 1.6.4
Requires:      php-pear(Archive_Tar) >= 1.3.8
Requires:      php-pear(HTTP_Request2) >= 2.1.1
Requires:      php-pear(PHP_CodeSniffer) >= 1.5.0
Requires:      php-pear(pear.pdepend.org/PHP_Depend) >= 0.10.0
Requires:      php-pear(pear.phpmd.org/PHP_PMD) >= 1.1.0
# Removed from package.xml as no more available in pear
Requires:      php-phpunit-PHPUnit
Requires:      php-phpunit-phpcpd

# TODO
# pear.phing.info/phingdocs >= 2.9.0
# VersionControl_SVN >= 0.4.0
# VersionControl_Git >= 0.4.3
# PEAR_PackageFileManager >= 1.5.2
# Services_Amazon_S3 >= 0.3.1
# pear.phpdoc.org/phpDocumentor >= 2.0.0a10

Provides:      php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:      php-composer(phing/phing) = %{version}
# The project/command
Provides:      phing = %{version}


%description
PHing Is Not GNU make; it's a project build system based on Apache Ant.

You can do anything with it that you could do with a traditional build
system like GNU make, and its use of simple XML build files and extensible
PHP "task" classes make it an easy-to-use and highly flexible build
framework. Features include file transformations (e.g. token replacement,
XSLT transformation, Smarty template transformations), file system operations,
interactive build support, SQL execution, CVS operations, tools for creating
PEAR packages, and much more.


%prep
%setup -qc
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

rm -rf %{buildroot}%{pear_metadir}/.??*

mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


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
%{_bindir}/phing
%doc %{pear_docdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{pear_phpdir}/%{pear_name}
%{pear_phpdir}/%{pear_name}.php
%{pear_xmldir}/%{name}.xml


%changelog
* Wed Oct 12 2016 Remi Collet <remi@fedoraproject.org> - 2.15.1-1
- Update to 2.15.1

* Thu Sep 15 2016 Remi Collet <remi@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0

* Fri Mar 11 2016 Remi Collet <remi@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0

* Fri Dec 04 2015 Remi Collet <remi@fedoraproject.org> - 2.13.0-1
- Update to 2.13.0
- provide phing

* Tue Aug 25 2015 Remi Collet <remi@fedoraproject.org> - 2.12.0-1
- Update to 2.12.0

* Wed May 20 2015 Remi Collet <remi@fedoraproject.org> - 2.11.0-1
- Update to 2.11.0

* Fri Feb 20 2015 Remi Collet <remi@fedoraproject.org> - 2.10.1-1
- Update to 2.10.1

* Fri Feb 13 2015 Remi Collet <remi@fedoraproject.org> - 2.10.0-1
- Update to 2.10.0

* Wed Dec 03 2014 Remi Collet <remi@fedoraproject.org> - 2.9.1-1
- Update to 2.9.1

* Wed Nov 26 2014 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0 (stable)

* Fri Oct 10 2014 Remi Collet <remi@fedoraproject.org> - 2.8.2-1
- Update to 2.8.2

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Wed May  1 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-3
- clean more non-free stuff

* Sat Apr 20 2013 Christof Damian <christof@damian.net> - 2.5.0-2
- remove more mentions of non-free stuff

* Thu Mar 28 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-2
- remove jsmin from task/defaults.properties

* Wed Mar 13 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Tue Jan 15 2013 Collet <RPMS@FamilleCollet.com> - 2.4.14-1.1
- sync with rawhide, drop non free stuff

* Mon Jan 14 2013 Christof Damian <christof@damian.net> - 2.4.14-1
- upstream 2.4.14
- remove non-free stuff
- remove optional xdebug requirement
- use pear_metadir

* Fri Nov 30 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.4.14-1
- upstream 2.4.14, for remi repo

* Tue Nov 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.4.13-1
- upstream 2.4.13, for remi repo
- add more requires (optional deps)

* Thu Apr 12 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.4.12-1
- upstream 2.4.13, backport for remi repo

* Wed Apr 11 2012 Christof Damian <christof@damian.net> - 2.4.12-1
- upstream 2.4.12

* Tue Jan 24 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.4.9-1
- upstream 2.4.9

* Fri Nov 04 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.8-1
- upstream 2.4.8, rebuild for remi repository
- doc in /usr/share/doc/pear

* Thu Nov  3 2011 Christof Damian <christof@damian.net> - 2.4.8-1
- upstream 2.4.8

* Sun Jul 17 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.4.6-1
- rebuild for remi repository

* Fri Jul 15 2011 Christof Damian <christof@damian.net> - 2.4.6-1
- upstream 2.4.6

* Sat Mar  5 2011 Christof Damian <christof@damian.net> - 2.4.5-1
- remove requires hint

* Fri Mar  4 2011 Christof Damian <christof@damian.net> - 2.4.5-1
- upstream 2.4.5

* Sun Dec 12 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.4-1
- rebuild for remi repository

* Wed Dec  8 2010 Christof Damian <christof@damian.net> - 2.4.4-1
- upstream 2.4.4

* Thu Nov 25 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.3-1
- rebuild for remi repository

* Tue Nov 23 2010 Christof Damian <christof@damian.net> - 2.4.3-1
- upstream 2.4.3

* Fri Aug 06 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.2-1
- rebuild for remi repository

* Sat Jul 31 2010 Christof Damian <christof@damian.net> - 2.4.2-1
- upstream 2.4.2

* Wed Jun 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 2.4.1-1
- rebuild for remi repository

* Thu May 27 2010 Christof Damian <christof@damian.net> - 2.4.1-1
- upstream 2.4.1
- taking over package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jul 19 2009 Remi Collet <RPMS@FamilleCollet.com> - 2.3.0-2
- rebuild for remi repository

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Nov  6 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-1
- stable version

* Tue Oct 30 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.1.RC2
- new release candidate version

* Tue Oct 16 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.1.RC1
- new release candidate version
- consequently adapted macros for all shell operations
- sanitized requires
- switched build root macro style
- additional s/\r\n/\n/g fixes

* Mon Sep  3 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.6.beta1
- name change (lowercase)
- changed pear datadir macro

* Fri Aug 24 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.5.beta1
- Fixed dos line terminators.

* Wed Aug 22 2007 Alexander Kahl <akahl@iconmobile.com> - 2.3.0-0.4.beta1
- New beta version.

* Tue Aug 21 2007 Alexander Kahl <akahl@iconmobile.com> - 2.2.0-3
- Adapted new Fedora layout.

* Tue Aug 21 2007 Alexander Kahl <akahl@iconmobile.com> - 2.2.0-2
- Updated PHPUnit dependency.

* Fri May 25 2007 Alexander Kahl <akahl@iconmobile.com> - 2.2.0-1
- Removed ant dependency.
- Added channel dependency.

* Wed May 23 2007 Alexander Kahl <akahl@iconmobile.com> 2.2.0-0
- Initial RPM release.
