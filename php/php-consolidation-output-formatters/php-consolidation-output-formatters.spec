# remirepo spec file for php-consolidation-output-formatters, from
#
# Fedora spec file for php-consolidation-output-formatters
#
# Copyright (c) 2016 Shawn Iwinski <shawn@iwin.ski>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     consolidation-org
%global github_name      output-formatters
%global github_version   2.0.1
%global github_commit    8bce15438a97afba5dcf036a71d961977b64fa3e

%global composer_vendor  consolidation
%global composer_project output-formatters

# "php": ">=5.4.0"
%global php_min_ver 5.4.0
# "symfony/console": "~2.5|~3.0"
# "symfony/finder": "~2.5|~3.0"
#     NOTE: Min version not 2.5 because autoloader required
%global symfony_min_ver 2.7.1
%global symfony_max_ver 4.0

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       Format text by applying transformations provided by plug-in formatters

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
BuildRequires: php-composer(symfony/console) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/console) >= %{symfony_min_ver}
BuildRequires: php-composer(symfony/finder) <  %{symfony_max_ver}
BuildRequires: php-composer(symfony/finder) >= %{symfony_min_ver}
## phpcompatinfo (computed from version 2.0.1)
BuildRequires: php-dom
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
%endif

# composer.json
Requires:      php(language) >= %{php_min_ver}
Requires:      php-composer(symfony/console) <  %{symfony_max_ver}
Requires:      php-composer(symfony/console) >= %{symfony_min_ver}
Requires:      php-composer(symfony/finder) <  %{symfony_max_ver}
Requires:      php-composer(symfony/finder) >= %{symfony_min_ver}
# phpcompatinfo (computed from version 2.0.1)
Requires:      php-dom
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.

Autoloader: %{phpdir}/Consolidation/OutputFormatters/autoload.php


%prep
%setup -qn %{github_name}-%{github_commit}


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Consolidation\\OutputFormatters\\', dirname(dirname(__DIR__)));

// Required dependencies
require_once '%{phpdir}/Symfony/Component/Console/autoload.php';
require_once '%{phpdir}/Symfony/Component/Finder/autoload.php';

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf   %{buildroot}

mkdir -p %{buildroot}%{phpdir}/Consolidation/OutputFormatters
cp -rp src/* %{buildroot}%{phpdir}/Consolidation/OutputFormatters/


%check
%if %{with_tests}
: Mock PSR-0 tests
mkdir -p tests-psr0/Consolidation
ln -s ../../tests/src tests-psr0/Consolidation/TestUtils

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader =
    require '%{buildroot}%{phpdir}/Consolidation/OutputFormatters/autoload.php';
$fedoraClassLoader->addPrefix('Consolidation\\TestUtils\\', __DIR__.'/tests-psr0');
BOOTSTRAP

run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit --bootstrap bootstrap.php || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
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
%dir %{phpdir}/Consolidation
     %{phpdir}/Consolidation/OutputFormatters


%changelog
* Tue Nov 01 2016 Shawn Iwinski <shawn@iwin.ski> - 2.0.1-1
- Update to 2.0.1 (RHBZ #1376274)

* Thu Jul 21 2016 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- backport for remi repository

* Tue Jul 19 2016 Shawn Iwinski <shawn@iwin.ski> - 1.0.0-1
- Initial package
