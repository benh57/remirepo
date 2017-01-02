# spec file for php-twig-ctwig
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:         %scl_package        php-twig-ctwig}
%{!?php_inidir: %global php_inidir  %{_sysconfdir}/php.d}
%{!?__pecl:     %global __pecl      %{_bindir}/pecl}
%{!?__php:      %global __php       %{_bindir}/php}

%global with_zts     0%{?__ztsphp:1}
%global pecl_name    CTwig
%global ext_name     twig
%global pecl_channel pear.twig-project.org
%if "%{php_version}" < "5.6"
%global ini_name     %{ext_name}.ini
%else
%global ini_name     40-%{ext_name}.ini
%endif

Summary:        Extension to improve performance of Twig
Name:           %{?scl_prefix}php-twig-ctwig
Version:        1.16.0
Release:        1%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
License:        BSD
Group:          Development/Languages
URL:            http://twig.sensiolabs.org
Source0:        http://%{pecl_channel}/get/%{pecl_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel >= 5.2.4
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  %{?scl_prefix}php-channel(%{pecl_channel})

Requires(post): %{__pecl}
Requires(postun): %{__pecl}
Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-channel(%{pecl_channel})

Provides:       %{?scl_prefix}php-%{ext_name} = %{version}
Provides:       %{?scl_prefix}php-%{ext_name}%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_channel}/%{pecl_name}) = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_channel}/%{pecl_name})%{?_isa} = %{version}
# Package have been renamed
Obsoletes:      %{?scl_prefix}php-twig-CTwig < 1.14.1-2
Provides:       %{?scl_prefix}php-twig-CTwig = %{version}-%{release}

%if 0%{?fedora} < 20
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Twig is a PHP template engine.

This package provides the Twig C extension (CTwig) to improve performance
of the Twig template language, used by Twig PHP extension (php-twig-Twig).


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

cd NTS
# Sanity check, really often broken
extver=$(sed -n '/#define PHP_TWIG_VERSION/{s/.* "//;s/".*$//;p}' php_twig.h)
if test "x${extver}" != "x%{version}%{?prever:-%{prever}}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}%{?prever:-%{prever}}.
   exit 1
fi
cd ..

%if %{with_zts}
# Duplicate source tree for NTS / ZTS build
cp -pr NTS ZTS
%endif

# Create configuration file
cat > %{ini_name} << 'EOF'
; Enable %{pecl_name} extension module
extension=%{ext_name}.so
EOF


%build
cd NTS
%{_bindir}/phpize
%configure \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# install config file
install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install XML package description
install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Documentation
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pear_docdir}/%{pecl_name}/$i
done


%post
%{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{pecl_uninstall} %{pecl_channel}/%{pecl_name} >/dev/null || :
fi


%check
: Minimal load test for NTS extension
%{__php} --no-php-ini \
    --define extension=NTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    --define extension=ZTS/modules/%{ext_name}.so \
    --modules | grep %{ext_name}
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pecl_name}
%{pecl_xmldir}/%{name}.xml
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{ext_name}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{ext_name}.so
%endif


%changelog
* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 1.16.0-1
- Update to 1.16.0

* Thu Apr 17 2014 Remi Collet <remi@fedoraproject.org> - 1.15.1-2
- add numerical prefix to extension configuration file (php 5.6)

* Fri Feb 14 2014 Remi Collet <remi@fedoraproject.org> - 1.15.1-1
- Update to 1.15.1

* Fri Dec 06 2013 Remi Collet <remi@fedoraproject.org> - 1.15.0-1
- Update to 1.15.0 (stable)
- move doc in pear doc_dir (this is not from pecl channel)

* Wed Oct 30 2013 Remi Collet <remi@fedoraproject.org> - 1.14.2-1
- Update to 1.14.2 (no change)
- install doc in pecl doc_dir

* Fri Oct 18 2013 Remi Collet <remi@fedoraproject.org> - 1.14.1-2
- rename from php-twig-CTwig to php-twig-ctwig

* Wed Oct 16 2013 Remi Collet <remi@fedoraproject.org> - 1.14.1-1
- Update to 1.14.1 (no change, only version bump)

* Sat Oct  5 2013 Remi Collet <rcollet@redhat.com> - 1.14.0-1
- adapt for SCL

* Thu Oct  3 2013 Remi Collet <remi@fedoraproject.org> - 1.14.0-1
- initial package
