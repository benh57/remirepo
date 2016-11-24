# Fedora spec file for php-ast
# Without SCL compatibility stuff, from:
#
# remirepo spec file for php-ast
#
# Copyright (c) 2015-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global gh_commit   abfef40846cb5454dafa1808769fde851ba8dd70
%global gh_short    %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner    nikic
%global gh_project  php-ast
%global pecl_name   ast
%global with_zts    0%{!?_without_zts:%{?__ztsphp:1}}
# After 20-tokenizer.ini
%global ini_name    40-%{pecl_name}.ini

Summary:       Abstract Syntax Tree
Name:          php-ast
Version:       0.1.2
Release:       1%{?dist}
License:       PHP
Group:         Development/Languages
URL:           https://github.com/%{gh_owner}/%{gh_project}
Source0:       https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRequires: php-devel > 7
BuildRequires: php-tokenizer

Requires:      php(zend-abi) = %{php_zend_api}
Requires:      php(api) = %{php_core_api}
Requires:      php-tokenizer%{?_isa}


%description
This extension exposes the abstract syntax tree generated by PHP 7.


%prep
%setup -qc
mv %{gh_project}-%{gh_commit} NTS

cd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_AST_VERSION/{s/.* "//;s/".*$//;p}' php_ast.h)
if test "x${extver}" != "x%{version}%{?gh_date:-dev}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?gh_date:-dev}.
   exit 1
fi
cd ..

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif

# Drop in the bit of configuration
cat << 'EOF' | tee %{ini_name}
; Enable '%{summary}' extension module
extension = %{pecl_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config \
    --enable-ast
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config \
    --enable-ast
make %{?_smp_mflags}
%endif


%install
# Install the NTS stuff
make -C NTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
# Install the ZTS stuff
make -C ZTS install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif



%check
cd NTS
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for NTS extension
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n -d extension=tokenizer.so -d extension=%{buildroot}%{php_extdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff || : ignore

%if %{with_zts}
cd ../ZTS
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: Upstream test suite  for ZTS extension
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n -d extension=tokenizer.so -d extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
%endif


%files
%license NTS/LICENSE
%doc NTS/EXPERIMENTAL
%doc NTS/README.md
%doc NTS/scripts
%doc NTS/util.php

%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%changelog
* Thu Nov 24 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-1
- drop SCL stuff for Fedora review

* Wed Sep 14 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-2
- rebuild for PHP 7.1 new API version

* Fri Aug  5 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-1
- update to 0.1.2

* Fri Jun 10 2016 Remi Collet <remi@fedoraproject.org> - 0.1.2-0.1.20160608gitb8f5805
- update to 0.1.2-dev for PHP 7.1

* Thu Jan  7 2016 Remi Collet <remi@fedoraproject.org> - 0.1.1-1
- update to 0.1.1

* Thu Oct 29 2015 Remi Collet <remi@fedoraproject.org> - 0.1.0-0.2.20151021gitac969d7
- add dependency on php-tokenizer, fix test suite

* Wed Oct 28 2015 Remi Collet <remi@fedoraproject.org> - 0.1.0-0.1.20151021gitac969d7
- new package, version 0.1.0dev
