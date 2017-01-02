# remirepo/fedora spec file for php-nette-bootstrap
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    1fc6e52b790864d2973d479a4460a89cec1f51f8
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   bootstrap
%global ns_vendor    Nette
%global ns_project   Bootstrap
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.3.5
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Bootstrap

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-tokenizer
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.2
# From composer.json, "require-dev": {
#        "nette/application": "~2.3",
#        "nette/caching": "~2.3",
#        "nette/database": "~2.3",
#        "nette/forms": "~2.3",
#        "nette/http": "~2.3",
#        "nette/mail": "~2.3",
#        "nette/robot-loader": "~2.2",
#        "nette/safe-stream": "~2.2",
#        "nette/security": "~2.3",
#        "nette/tester": "~1.3",
#        "latte/latte": "~2.2",
#        "tracy/tracy": "~2.3"
# ignore not yet available components
BuildRequires:  php-composer(%{gh_owner}/application) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/caching) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/database) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/forms) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/http) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/mail) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/robot-loader) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/safe-stream) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/security) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.3
BuildRequires:  php-composer(latte/latte) >= 2.2
BuildRequires:  php-composer(tracy/tracy) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.3
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
#        "nette/di": "~2.3.0",
#        "nette/utils": "~2.2"
Requires:       php(language) >= 5.3.1
Requires:       php-tokenizer
Requires:       php-composer(%{gh_owner}/di) >= 2.3
Requires:       php-composer(%{gh_owner}/di) <  2.4
Requires:       php-composer(%{gh_owner}/utils) >= 2.2
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.3
Requires:       php-reflection
Requires:       php-pcre
%if 0%{?fedora} > 21
Suggests:       php-pecl(memcache)
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Loads Nette Framework and all libraries.

Class Configurator creates so called DI container
and handles application initialization.

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Utils/autoload.php';
EOF


%install
rm -rf       %{buildroot}
mkdir -p     %{buildroot}%{php_home}/%{ns_vendor}
cp -pr src/* %{buildroot}%{php_home}/%{ns_vendor}/


%check
%if %{with_tests}
: Generate configuration
cat /etc/php.ini /etc/php.d/*ini >php.ini
export LANG=fr_FR.utf8

: Generate autoloader
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Tester/autoload.php';
require_once '%{php_home}/Latte/autoload.php';
require_once '%{php_home}/Tracy/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Application/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Caching/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Database/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Forms/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Http/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Mail/autoload.php';
require_once '%{php_home}/%{ns_vendor}/RobotLoader/autoload.php';
require_once '%{php_home}/%{ns_vendor}/SafeStream/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Security/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
nette-tester --colors 0 -p php -c ./php.ini tests -s

# remirepo:4
if which php70; then
  cat /etc/opt/remi/php70/php.ini /etc/opt/remi/php70/php.d/*ini >php.ini
  php70 %{_bindir}/nette-tester --colors 0 -p php70 -c ./php.ini tests -s
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license license.md
%doc readme.md contributing.md
%doc composer.json
%{php_home}/%{ns_vendor}/%{ns_project}
%{php_home}/%{ns_vendor}/Bridges/Framework


%changelog
* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- update to 2.3.5

* Mon Nov 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- update to 2.3.4

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-2
- more tests

* Tue Oct 20 2015 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- initial package
