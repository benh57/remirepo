# remirepo spec file for php-swiftmailer
#
# Copyright (c) 2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please preserve changelog entries
#
%global gh_commit    0697e6aa65c83edf97bb0f23d8763f94e3f11421
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     swiftmailer
%global gh_project   swiftmailer
%global with_tests   0%{!?_without_tests:1}
%global php_home     %{_datadir}/php

Name:           php-%{gh_project}
Version:        5.4.1
Release:        1%{?dist}
Summary:        Free Feature-rich PHP Mailer

Group:          Development/Libraries
License:        MIT
URL:            http://www.swiftmailer.org/
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

# Upstream patches
# Fix test bootstrap and disable gc to avoid segfault
Patch0:         %{gh_project}-upstream.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
BuildRequires:  php-composer(phpunit/phpunit)
BuildRequires:  php-composer(theseer/autoload)
# From composer.json, "require-dev": {
#        "mockery/mockery": "~0.9.1,<0.9.4"
BuildRequires:  php-composer(mockery/mockery) >= 0.9.1
BuildRequires:  php-composer(mockery/mockery) <  0.9.4
%endif

# From composer.json, "require": {
#        "php": ">=5.3.3"
Requires:       php(language) >= 5.3.3
# from phpcompatinfo report on version 5.4.1
Requires:       php-bcmath
Requires:       php-ctype
Requires:       php-date
Requires:       php-hash
Requires:       php-iconv
Requires:       php-mbstring
Requires:       php-mcrypt
Requires:       php-mhash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-simplexml
Requires:       php-spl

# Removal for official repo not yet planed
%if 0%{?fedora} > 99
Obsoletes:      php-swift-Swift   <= 5.4.1
# Single package in this channel
Obsoletes:      php-channel-swift <= 1.3
Provides:       php-pear(pear.swiftmailer.org/Swift) = %{version}
%endif

Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Swift Mailer integrates into any web app written in PHP, offering a 
flexible and elegant object-oriented approach to sending emails with 
a multitude of features.

Autoloader: %{php_home}/Swift/swift_required.php



%prep
%setup -q -n %{gh_project}-%{gh_commit}

%patch0 -p1

# Install using the same layout than the old PEAR package
mv lib/swift_required_pear.php lib/swift_required.php
rm lib/swiftmailer_generate_mimes_config.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}

mkdir -p                   %{buildroot}/%{php_home}/Swift
cp -p lib/*.php            %{buildroot}/%{php_home}/Swift/
cp -pr lib/classes/*       %{buildroot}/%{php_home}/Swift/
cp -pr lib/dependency_maps %{buildroot}/%{php_home}/Swift/


%check
%if %{with_tests}
: Use installed tree and autoloader
mkdir vendor
%{_bindir}/phpab --output vendor/autoload.php tests
cat << 'EOF' | tee -a vendor/autoload.php
require_once '%{buildroot}/%{php_home}/Swift/swift_required.php';
require_once '/usr/share/php/Mockery/autoload.php';
EOF

TMPDIR=$(mktemp -d $PWD/rpmtests-XXXXXXXX)
cat << EOF | tee tests/acceptance.conf.php
<?php
define('SWIFT_TMP_DIR', '$TMPDIR');
EOF

ret=0

: Run upstream test suite
%{_bindir}/phpunit --exclude smoke --verbose || ret=1

if which php70; then
   php70 %{_bindir}/phpunit --exclude smoke --verbose || : ignore PHP 7 test results
fi
%endif

# Cleanup
rm -r $TMPDIR


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc CHANGES README
%doc doc
%doc composer.json
%{php_home}/Swift


%changelog
* Fri Oct 16 2015 Remi Collet <remi@fedoraproject.org> - 5.4.1-1
- initial rpm, version 5.4.1
- sources from github, pear channel is dead
