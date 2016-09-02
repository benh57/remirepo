# remirepo/fedora spec file for php-horde-Horde-Queue
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Queue
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Queue
Version:        1.1.4
Release:        1%{?dist}
Summary:        Horde Queue

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-queue) = %{version}


%description
Queue layer with various storage backends and runners


%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


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
%dir %{pear_phpdir}/Horde
%{pear_phpdir}/Horde/Queue
%{pear_datadir}/%{pear_name}


%changelog
* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2
- add provides php-composer(horde/horde-queue)

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 1.0.0-1
- New Package
