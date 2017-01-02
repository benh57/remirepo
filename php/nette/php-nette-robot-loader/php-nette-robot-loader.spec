# remirepo/fedora spec file for php-nette-robot-loader
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit    0dbed866df47fd0425ce9a3cc9085779d8ada143
#global gh_date      20150728
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     nette
%global gh_project   robot-loader
%global ns_vendor    Nette
%global ns_project   RobotLoader
%global php_home     %{_datadir}/php
%global with_tests   0%{!?_without_tests:1}

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.3.2
%global specrel 1
Release:        %{?gh_date:0.%{specrel}.%{?prever}%{!?prever:%{gh_date}git%{gh_short}}}%{!?gh_date:%{specrel}}%{?dist}
Summary:        Nette RobotLoader: comfortable autoloading

Group:          Development/Libraries
License:        BSD or GPLv2 or GPLv3
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{name}-%{version}-%{gh_short}.tgz
# pull a git snapshot to get test sutie
Source1:        makesrc.sh

# Ensure TEMP_DIR exists
Patch0:         %{name}-rpm.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-composer(theseer/autoload)
%if %{with_tests}
BuildRequires:  php(language) >= 5.3.1
BuildRequires:  php-composer(%{gh_owner}/caching) >= 2.2
BuildRequires:  php-composer(%{gh_owner}/finder) >= 2.3
BuildRequires:  php-composer(%{gh_owner}/utils) >= 2.2
BuildRequires:  php-pcre
BuildRequires:  php-phar
BuildRequires:  php-spl
# From composer.json, "require-dev": {
#        "nette/tester": "~1.4"
BuildRequires:  php-composer(%{gh_owner}/tester) >= 1.4
%endif

# from composer.json, "require": {
#        "php": ">=5.3.1"
#        "nette/caching": "~2.2",
#        "nette/finder": "~2.3",
#        "nette/utils": "~2.2"
Requires:       php(language) >= 5.3.1
Requires:       php-composer(%{gh_owner}/caching) >= 2.2
Requires:       php-composer(%{gh_owner}/caching) <  3
Requires:       php-composer(%{gh_owner}/finder) >= 2.3
Requires:       php-composer(%{gh_owner}/finder) <  3
Requires:       php-composer(%{gh_owner}/utils) >= 2.2
Requires:       php-composer(%{gh_owner}/utils) <  3
# from phpcompatinfo report for version 2.3.1
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
RobotLoader is a tool that gives you comfort of automated class loading
for your entire application including third-party libraries.

- get rid of all require
- only necessary scripts are loaded
- requires no strict file naming conventions
- allows more classes in single file

To use this library, you just have to add, in your project:
  require_once '%{php_home}/%{ns_vendor}/%{ns_project}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p0 -b .rpm


%build
: Generate a classmap autoloader
phpab --output src/%{ns_project}/autoload.php src

cat << 'EOF' | tee -a src/%{ns_project}/autoload.php
// Dependencies
require_once '%{php_home}/%{ns_vendor}/Caching/autoload.php';
require_once '%{php_home}/%{ns_vendor}/Finder/autoload.php';
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


%changelog
* Mon Jun 20 2016 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- update to 2.3.2

* Tue Nov  3 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-2
- fix package summary

* Fri Oct 30 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- initial package
