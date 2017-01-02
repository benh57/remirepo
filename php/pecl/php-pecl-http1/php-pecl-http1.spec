# spec file for php-pecl-http1
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package         php-pecl-http1}
%{!?scl:         %global _root_prefix %{_prefix}}

# The project is pecl_http but the extension is only http
%global proj_name pecl_http
%global pecl_name http
%global with_zts  0%{?__ztsphp:1}

# php-pecl-http exists and is version 2
Name:           %{?scl_prefix}php-pecl-http1
Version:        1.7.6
Release:        6%{?dist}%{!?nophptag:%(%{__php} -r 'echo ".".PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')}
Summary:        Extended HTTP support

License:        BSD
Group:          Development/Languages
URL:            http://pecl.php.net/package/pecl_http
Source0:        http://pecl.php.net/get/%{proj_name}-%{version}.tgz

# Change for package
Patch0:         %{pecl_name}-ini.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{?scl_prefix}php-devel
BuildRequires:  %{?scl_prefix}php-hash
BuildRequires:  %{?scl_prefix}php-iconv
BuildRequires:  %{?scl_prefix}php-session
BuildRequires:  %{?scl_prefix}php-pear
BuildRequires:  pcre-devel
BuildRequires:  zlib-devel
BuildRequires:  curl-devel
%if 0%{?scl:1} && 0%{?fedora} < 15 && 0%{?rhel} < 7 && "%{?scl_vendor}" != "remi"
# Filter in the SCL collection
%{?filter_requires_in: %filter_requires_in %{_libdir}/.*\.so}
# libvent from SCL as not available in system
BuildRequires: %{?scl_prefix}libevent-devel  >= 2.0.2
Requires:      %{?scl_prefix}libevent%{_isa} >= 2.0.2
Requires:      libcurl%{_isa}
%global        _event_prefix %{_prefix}
%else
BuildRequires: libevent-devel >= 2.0.2
%global        _event_prefix %{_root_prefix}
%endif

Requires:       %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:       %{?scl_prefix}php(api) = %{php_core_api}
Requires:       %{?scl_prefix}php-hash%{?_isa}
Requires:       %{?scl_prefix}php-iconv%{?_isa}
Requires:       %{?scl_prefix}php-session%{?_isa}
# From phpcompatinfo on the PHP extension (pgsql is optional)
Requires:       %{?scl_prefix}php-date%{?_isa}
Requires:       %{?scl_prefix}php-pcre%{?_isa}
Requires:       %{?scl_prefix}php-xmlrpc%{?_isa}
%{?_sclreq:Requires: %{?scl_prefix}runtime%{?_sclreq}%{?_isa}}

# From upstream documentation
Conflicts:      %{?scl_prefix}php-pecl-event
# Can't install both version of the same extension
Conflicts:      %{?scl_prefix}php-pecl-http

Provides:       %{?scl_prefix}php-pecl(%{proj_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{proj_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})         = %{version}
Provides:       %{?scl_prefix}php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{?scl_prefix}php-pecl-http1                 = %{version}-%{release}
Provides:       %{?scl_prefix}php-pecl-http1%{?_isa}         = %{version}-%{release}
Provides:       %{?scl_prefix}php-%{pecl_name}               = %{version}
Provides:       %{?scl_prefix}php-%{pecl_name}%{?_isa}       = %{version}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter shared private
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
The HTTP extension aims to provide a convenient and powerful set of
functionality for major applications.

The HTTP extension eases handling of HTTP URLs, dates, redirects, headers
and messages in a HTTP context (both incoming and outgoing). It also provides
means for client negotiation of preferred language and charset, as well as
a convenient way to exchange arbitrary data with caching and resuming
capabilities.

It provides powerful request functionality, if built with CURL
support. Parallel requests are available for PHP 5 and greater.

Note:
. %{?scl_prefix}php-pecl-http1 provides API version 1
. %{?scl_prefix}php-pecl-http  provides API version 2

Package built for PHP %(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')%{?scl: as Software Collection (%{scl} by %{?scl_vendor}%{!?scl_vendor:rh})}.


%package devel
Summary:       Extended HTTP support developer files (header)
Group:         Development/Libraries
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      %{?scl_prefix}php-devel%{?_isa}
# Can't install both version of the same extension
Conflicts:     %{?scl_prefix}php-pecl-http-devel

%description devel
These are the files needed to compile programs using HTTP extension.


%prep
%setup -c -q 

%{?_licensedir:sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml}

mv %{proj_name}-%{version} NTS
cd NTS
%patch0 -p1 -b .rpmconf

extver=$(sed -n '/#define PHP_HTTP_VERSION/{s/.* "//;s/".*$//;p}' php_http.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream HTTP version is now ${extver}, expecting %{version}.
   : Update the pdover macro and rebuild.
   exit 1
fi
cd ..

%if %{with_zts}
cp -pr NTS ZTS
%endif


%build
cd NTS
%{_bindir}/phpize
%configure \
  --with-http-libcurl-dir=%{_root_prefix} \
  --with-http-curl-libevent=%{_event_prefix} \
  --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

%if %{with_zts}
cd ../ZTS
%{_bindir}/zts-phpize
%configure \
  --with-http-libcurl-dir=%{_root_prefix} \
  --with-http-curl-libevent=%{_event_prefix} \
  --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
%endif


%install
rm -rf %{buildroot}

make -C NTS install INSTALL_ROOT=%{buildroot}

# Install XML package description
install -Dpm 644 package.xml %{buildroot}%{pecl_xmldir}/%{name}.xml

# install config file (z-http.ini to be loaded after hash/iconv/session)
install -Dpm644 NTS/docs/%{pecl_name}.ini \
        %{buildroot}%{php_inidir}/z-%{pecl_name}.ini

%if %{with_zts}
make -C ZTS install INSTALL_ROOT=%{buildroot}

install -Dpm644 ZTS/docs/%{pecl_name}.ini \
        %{buildroot}%{php_ztsinidir}/z-%{pecl_name}.ini
%endif

# Test & Documentation
for i in $(grep 'role="test"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_testdir}/%{proj_name}/$i
done
for i in $(grep 'role="doc"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pecl_docdir}/%{proj_name}/${i#docs/}
done

# PHP Library
for i in $(grep 'role="php"' package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 NTS/$i %{buildroot}%{pear_phpdir}/pecl/http/$(basename $i)
done

# RPM/PEAR consistency, to be checked after install
# pecl list-files pecl_http | while read a b c; do [ -n "$b" -a -z "$c" -a ! -f "$b" ] && echo missing $b; done


%check
# Add needed extensions
modules=""
for mod in hash iconv session; do
  if [ -f %{php_extdir}/${mod}.so ]; then
    modules="$modules --define extension=${mod}.so"
  fi
done

: Minimal load test for NTS extension
%{__php} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

%if %{with_zts}
: Minimal load test for ZTS extension
%{__ztsphp} --no-php-ini \
    $modules \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif


%if 0%{?fedora} < 24
# when pear installed alone, after us
%triggerin -- %{?scl_prefix}php-pear
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

# posttrans as pear can be installed after us
%posttrans
if [ -x %{__pecl} ] ; then
    %{pecl_install} %{pecl_xmldir}/%{name}.xml >/dev/null || :
fi

%postun
if [ $1 -eq 0 -a -x %{__pecl} ] ; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{?_licensedir:%license NTS/LICENSE}
%doc     %{pecl_docdir}/%{proj_name}
%exclude %{pecl_docdir}/%{proj_name}/examples
%config(noreplace) %{php_inidir}/z-%{pecl_name}.ini
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{name}.xml

%dir %{pear_phpdir}/pecl
%{pear_phpdir}/pecl/http

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/z-%{pecl_name}.ini
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%defattr(-,root,root,-)
%doc %{pecl_docdir}/%{proj_name}/examples
%doc %{pecl_testdir}/%{proj_name}
%{php_incldir}/ext/%{pecl_name}
%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Thu Mar 10 2016 Remi Collet <remi@fedoraproject.org> - 1.7.6-6
- adapt for F24
- drop runtime dependency on pear, new scriptlets
- fix license management

* Wed Dec 24 2014 Remi Collet <remi@fedoraproject.org> - 1.7.6-5.1
- Fedora 21 SCL mass rebuild

* Mon Sep  1 2014 Remi Collet <remi@fedoraproject.org> - 1.7.6-5
- improve SCL build

* Thu Nov  7 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-4
- fix dependencies for EPEL-6

* Tue Oct 22 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-3
- install doc in pecl doc_dir
- install tests in pecl test_dir
- install PHP library in /usr/share/pear/pecl/http

* Thu Aug  1 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-2
- cleanups, adapt for SCL, make ZTS optional

* Thu Jun 20 2013 Remi Collet <remi@fedoraproject.org> - 1.7.6-1
- Update to 1.7.6

* Thu Mar 21 2013 Remi Collet <remi@fedoraproject.org> - 1.7.5-1
- initial package
