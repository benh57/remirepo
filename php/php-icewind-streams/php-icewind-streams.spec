# remirepo/fedora spec file for php-icewind-streams
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
# Github information
%global gh_commit    6bfd2fdbd99319f5e010d0a684409189a562cb1e
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     icewind1991
%global gh_project   Streams
# Packagist information
%global pk_vendor    icewind
%global pk_name      streams
# Namespace information
%global ns_vendor    Icewind
%global ns_name      Streams

Name:           php-%{pk_vendor}-%{pk_name}
Version:        0.5.2
Release:        1%{?dist}
Summary:        A set of generic stream wrappers

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        %{url}/archive/%{gh_commit}/%{name}-%{version}-%{gh_short}.tar.gz
Source1:        %{name}-autoload.php

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
# For tests
BuildRequires:  php(language) >= 5.3
# From composer.json, "require-dev": {
#		"satooshi/php-coveralls": "v1.0.0",
#		"phpunit/phpunit": "^4.8"
BuildRequires:  php-composer(phpunit/phpunit) >= 4.8
BuildRequires:  php-composer(theseer/autoload)
# Autoloader
BuildRequires:  php-composer(fedora/autoloader)

# From composer.json, "require": {
#      "php": ">=5.3"
Requires:       php(language) >= 5.3
# From phpcompatinfo report for version 0.2.0
Requires:       php-spl
# Autoloader
Requires:       php-composer(fedora/autoloader)

Provides:       php-composer(%{pk_vendor}/%{pk_name}) = %{version}


%description
Generic stream wrappers for php.

To use this library, you just have to add, in your project:
  require-once '%{_datadir}/php/%{ns_vendor}/%{ns_name}/autoload.php';


%prep
%setup -q -n %{gh_project}-%{gh_commit}

cp %{SOURCE1} src/autoload.php


%build
# Empty build section, most likely nothing required.


%install
rm -rf     %{buildroot}
# Restore PSR-0 tree
mkdir -p   %{buildroot}%{_datadir}/php/%{ns_vendor}
cp -pr src %{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_name}



%check
cd tests
: Generate a simple autoloader for test suite
%{_bindir}/phpab --output bootstrap.php .
echo "require '%{buildroot}%{_datadir}/php/%{ns_vendor}/%{ns_name}/autoload.php';" >> bootstrap.php

: Run the test suite
# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose
# remirepo:2
fi
exit $ret


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENCE
%doc composer.json
%doc *.md
%dir %{_datadir}/php/%{ns_vendor}
     %{_datadir}/php/%{ns_vendor}/%{ns_name}


%changelog
* Mon Dec  5 2016 Remi Collet <remi@fedoraproject.org> - 0.5.2-1
- update to 0.5.2

* Thu Oct 27 2016 Remi Collet <remi@fedoraproject.org> - 0.5.1-1
- update to 0.5.1
- switch from symfony/class-loader to fedora/autoloader

* Fri Jun  3 2016 Remi Collet <remi@fedoraproject.org> - 0.4.1-1
- update to 0.4.1

* Thu Mar 17 2016 Remi Collet <remi@fedoraproject.org> - 0.4.0-1
- update to 0.4.0

* Wed Sep  9 2015 Remi Collet <remi@fedoraproject.org> - 0.3.0-1
- version 0.3.0

* Tue Sep  1 2015 Remi Collet <remi@fedoraproject.org> - 0.2.0-1
- initial package, version 0.2.0
