# remirepo/fedora spec file for php-nette-security
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    779254a5484a106344a81c8cb9ce2b8570e38f34
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   security
%global ns_vendor    Nette
%global ns_project   Security
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.3.2
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette Security: Access Control Component

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
BuildRequires:  php-pcre
BuildRequires:  php-session
BuildRequires:  php-spl
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.2
# From composer.json, "require-dev": {
#        "nette/di": "~2.3",
#        "nette/http": "~2.3",
#        "nette/tester": "~1.4"
BuildRequires:  php-composer(%{gh_owner}/di) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/http) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.4
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
#        "nette/utils": "~2.2"
Requires:       php(language) >= 5.3.1
Requires:       php-composer(%{gh_owner}/utils) >= 2.2
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.1
Requires:       php-pcre
Requires:       php-session
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Nette Security: Access Control
- user login and logout
- verifying user privileges
- securing against vulnerabilities
- how to create custom authenticators and authorizators
- Access Control List

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
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
require_once '%{php_home}/%{ns_vendor}/DI/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Http/autoload.php';
require_once '%{buildroot}%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';
EOF

: Run test suite in sources tree
nette-tester --colors 0 -p php -c ./php.ini tests -s

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
%{php_home}/%{ns_vendor}/Bridges


%changelog
* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- initial package
