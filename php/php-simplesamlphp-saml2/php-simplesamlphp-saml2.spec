# remirepo spec file for php-simplesamlphp-saml2, from:
#
# Fedora spec file for php-simplesamlphp-saml2
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve the changelog entries
#

%global github_owner     simplesamlphp
%global github_name      saml2
%global github_version   2.3.4
%global github_commit    967edad97f38578f9b4561d6f624c974dd2c14a9

%global composer_vendor  simplesamlphp
%global composer_project saml2

# "php": ">=5.3.3"
%global php_min_ver 5.3.3
# "mockery/mockery": "~0.9"
%global mockery_min_ver 0.9
%global mockery_max_ver 1.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.1
%global psr_log_max_ver 2.0
# "robrichards/xmlseclibs": "^2.0"
%global robrichards_xmlseclibs_min_ver 2.0
%global robrichards_xmlseclibs_max_ver 3.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       SAML2 PHP library from SimpleSAMLphp

Group:         Development/Libraries
License:       LGPLv2
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                        >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(psr/log)                >= %{psr_log_min_ver}
BuildRequires: php-composer(robrichards/xmlseclibs) >= %{robrichards_xmlseclibs_min_ver}
BuildRequires: php-dom
BuildRequires: php-openssl
BuildRequires: php-composer(mockery/mockery)        >= %{mockery_min_ver}
## phpcompatinfo (computed from version 2.3.4)
BuildRequires: php-date
BuildRequires: php-libxml
BuildRequires: php-mcrypt
BuildRequires: php-pcre
BuildRequires: php-spl
BuildRequires: php-zlib
## Autoloader
BuildRequires: php-composer(fedora/autoloader)
%endif

# composer.json
Requires:      php(language)                        >= %{php_min_ver}
Requires:      php-composer(psr/log)                <  %{psr_log_max_ver}
Requires:      php-composer(psr/log)                >= %{psr_log_min_ver}
Requires:      php-composer(robrichards/xmlseclibs) <  %{robrichards_xmlseclibs_max_ver}
Requires:      php-composer(robrichards/xmlseclibs) >= %{robrichards_xmlseclibs_min_ver}
Requires:      php-dom
Requires:      php-openssl
# phpcompatinfo (computed from version 2.3.4)
Requires:      php-date
Requires:      php-libxml
Requires:      php-pcre
Requires:      php-spl
Requires:      php-zlib
# Autoloader
Requires:      php-composer(fedora/autoloader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}


%description
A PHP library for SAML2 related functionality. Extracted from SimpleSAMLphp [1],
used by OpenConext [2]. This library started as a collaboration between
UNINETT [3] and SURFnet [4] but everyone is invited to contribute.

Autoloader: %{phpdir}/SAML2/autoload.php

[1] https://www.simplesamlphp.org/
[2] https://www.openconext.org/
[3] https://www.uninett.no/
[4] https://www.surfnet.nl/


%prep
%setup -qn %{github_name}-%{github_commit}

: Remove upstream temporary autoloader
rm -f src/_autoload.php


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/SAML2/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 */
require_once '%{phpdir}/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('SAML2\\', __DIR__);

\Fedora\Autoloader\Dependencies::required(array(
    '%{phpdir}/Psr/Log/autoload.php',
    '%{phpdir}/RobRichards/XMLSecLibs/autoload.php',
));
AUTOLOAD


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Create pseudo Composer autoloader
mkdir vendor
cat <<'AUTOLOAD' | tee vendor/autoload.php
<?php
require '%{buildroot}%{phpdir}/SAML2/autoload.php';
\Fedora\Autoloader\Autoload::addPsr4('SAML2\\', dirname(__DIR__).'/tests/SAML2');
require_once '%{phpdir}/Mockery/autoload.php';
AUTOLOAD

: Run tests
ret=0
run=0
if which php56; then
   php56 %{_bindir}/phpunit --configuration=tools/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --configuration=tools/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --configuration=tools/phpunit --verbose
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/SAML2


%changelog
* Thu Dec 15 2016 Shawn Iwinski <shawn@iwin.ski> - 2.3.4-1
- Update to 2.3.4 (RHBZ #1405027)

* Sat Dec 03 2016 Shawn Iwinski <shawn@iwin.ski> - 2.3.3-1
- Update to 2.3.3 (RHBZ #1401147)
- 201612-01 (https://simplesamlphp.org/security/201612-01)

* Fri Dec  2 2016 Remi Collet <remi@remirepo.net> - 2.3.3-1
- update to 2.3.3

* Wed Nov 09 2016 Shawn Iwinski <shawn@iwin.ski> - 2.3.2-1
- Update to 2.3.2 (RHBZ #1393368)
- Change autoloader from php-composer(symfony/class-loader) to
  php-composer(fedora/autoloader)

* Wed Nov  9 2016 Remi Collet <remi@remirepo.net> - 2.3.2-1
- update to 2.3.2

* Wed Nov  9 2016 Remi Collet <remi@remirepo.net> - 2.3.1-1
- update to 2.3.1

* Sun Sep 25 2016 Shawn Iwinski <shawn@iwin.ski> - 2.3-1
- Update to 2.3 (RHBZ #1376301)

* Sat Jul 30 2016 Remi Collet <remi@remirepo.net> - 2.2-2
- backport for remirepo

* Fri Jul 29 2016 Shawn Iwinski <shawn@iwin.ski> - 2.2-2
- Remove upstream temporary autoloader

* Sun Jul 10 2016 Shawn Iwinski <shawn@iwin.ski> - 2.2-1
- Initial package
