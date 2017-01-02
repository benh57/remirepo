# remirepo/fedora spec file for php-horde-Horde-Editor
#
# Copyright (c) 2013-2017 Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Editor
%global pear_channel pear.horde.org
%global sysckeditor  0

Name:           php-horde-Horde-Editor
Version:        2.0.4
Release:        3%{?dist}
Summary:        Horde Editor API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
%if %{sysckeditor}
Requires:       ckeditor
%else
Provides:       horde-ckeditor
%endif
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Browser) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
The Horde_Editor package provides an API to generate the code necessary for
embedding javascript RTE editors in a web page.


%prep
%setup -q -c

cd %{pear_name}-%{version}
%if %{sysckeditor}
sed -e '/name="js/d' \
    ../package.xml >%{name}.xml

if [ ! -d  js/ckeditor ]; then
   : Check js/ckeditor path
   exit 1
fi
%else
mv ../package.xml %{name}.xml
%endif


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Editor
%{pear_phpdir}/Horde/Editor.php
%if ! %{sysckeditor}
%dir %{pear_hordedir}/js
%{pear_hordedir}/js/ckeditor
%endif

%changelog
* Wed Jul 09 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-3
- use bundled ckeditor

* Tue Mar 04 2014 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (no change)

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2 for remi repo
- drop merged patch for http://bugs.horde.org/ticket/11950

* Thu Jan 24 2013 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- use Alias for system JS

* Sat Jan 12 2013 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Initial package
