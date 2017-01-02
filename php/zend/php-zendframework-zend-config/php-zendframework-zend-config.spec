# remirepo/Fedora spec file for php-zendframework-zend-config
#
# Copyright (c) 2015-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global bootstrap    0
%global gh_commit    2920e877a9f6dca9fa8f6bd3b1ffc2e19bb1e30d
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     zendframework
%global gh_project   zend-config
%global php_home     %{_datadir}/php
%global library      Config
%if %{bootstrap}
%global with_tests   0%{?_with_tests:1}
%else
%global with_tests   0%{!?_without_tests:1}
%endif

Name:           php-%{gh_owner}-%{gh_project}
Version:        2.6.0
Release:        1%{?dist}
Summary:        Zend Framework %{library} component

Group:          Development/Libraries
License:        BSD
URL:            https://zendframework.github.io/%{gh_project}/
Source0:        %{gh_commit}/%{name}-%{version}-%{gh_short}.tgz
Source1:        makesrc.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
# Tests
%if %{with_tests}
BuildRequires:  php(language) >= 5.5
BuildRequires:  php-libxml
BuildRequires:  php-pcre
BuildRequires:  php-spl
BuildRequires:  php-xmlreader
BuildRequires:  php-xmlwriter
BuildRequires:  php-composer(%{gh_owner}/zend-loader) >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-stdlib) >= 2.7
# From composer, "require-dev": {
#        "zendframework/zend-filter": "^2.6",
#        "zendframework/zend-i18n": "^2.5",
#        "zendframework/zend-json": "^2.6.1",
#        "zendframework/zend-servicemanager": "^2.7.5 || ^3.0.3",
#        "fabpot/php-cs-fixer": "1.7.*",
#        "phpunit/PHPUnit": "~4.0"
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-i18n)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-json)             >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-servicemanager)   >= 2.5
BuildRequires:  php-composer(%{gh_owner}/zend-filter)           >= 2.5
BuildRequires:  php-composer(phpunit/phpunit)                   >= 4.0
%endif

# From composer, "require": {
#        "php": "^5.5 || ^7.0",
#        "zendframework/zend-stdlib": "^2.7 || ^3.0"
Requires:       php(language) >= 5.5
Requires:       php-composer(%{gh_owner}/zend-stdlib) >= 2.7
Requires:       php-composer(%{gh_owner}/zend-stdlib) <  4
# From phpcompatinfo report for version 2.5.2
Requires:       php-libxml
Requires:       php-pcre
Requires:       php-spl
Requires:       php-xmlreader
Requires:       php-xmlwriter
%if ! %{bootstrap}
# From composer, "suggest": {
#        "zendframework/zend-filter": "Zend\\Filter component",
#        "zendframework/zend-i18n": "Zend\\I18n component",
#        "zendframework/zend-json": "Zend\\Json to use the Json reader or writer classes",
#        "zendframework/zend-servicemanager": "Zend\\ServiceManager for use with the Config Factory to retrieve reader and writer instances"
%if 0%{?fedora} >= 21
Suggests:       php-composer(%{gh_owner}/zend-filter)
Suggests:       php-composer(%{gh_owner}/zend-i18n)
Suggests:       php-composer(%{gh_owner}/zend-json)
Suggests:       php-composer(%{gh_owner}/zend-servicemanager)
%endif
%endif

Obsoletes:      php-ZendFramework2-%{library} < 2.5
Provides:       php-ZendFramework2-%{library} = %{version}
Provides:       php-composer(%{gh_owner}/%{gh_project}) = %{version}


%description
Zend\Config is designed to simplify access to configuration data within
applications. It provides a nested object property-based user interface
for accessing this configuration data within application code. The
configuration data may come from a variety of media supporting hierarchical
data storage.

Documentation: https://zendframework.github.io/%{gh_project}/


%prep
%setup -q -n %{gh_project}-%{gh_commit}

mv LICENSE.md LICENSE


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p   %{buildroot}%{php_home}/Zend/
cp -pr src %{buildroot}%{php_home}/Zend/%{library}


%check
%if %{with_tests}
mkdir vendor
cat << 'EOF' | tee vendor/autoload.php
<?php
require_once '%{php_home}/Zend/Loader/AutoloaderFactory.php';
Zend\Loader\AutoloaderFactory::factory(array(
    'Zend\Loader\StandardAutoloader' => array(
        'namespaces' => array(
           'ZendTest\\Config' => dirname(__DIR__).'/test/',
           'Zend\\Config'     => '%{buildroot}%{php_home}/Zend/%{library}'
))));
require_once '%{php_home}/Zend/autoload.php';
EOF

%{_bindir}/phpunit --include-path=%{buildroot}%{php_home}

if which php70; then
   php70 %{_bindir}/phpunit --include-path=%{buildroot}%{php_home}
fi
%else
: Test suite disabled
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md
%doc composer.json
%{php_home}/Zend/%{library}


%changelog
* Fri Feb  5 2016 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- update to 2.6.0
- raise dependency on PHP >= 5.5
- raise dependency on zend-stdlib >= 2.7

* Tue Aug  4 2015 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- initial package
