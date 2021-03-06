%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name   Sabre_HTTP
%global channelname pear.sabredav.org
%global mainver     1.7.13

Name:           php-sabredav-Sabre_HTTP
Epoch:          1
Version:        1.7.11
Release:        1%{?dist}
Summary:        HTTP component for the SabreDAV WebDAV framework for PHP

Group:          Development/Libraries
License:        BSD
URL:            http://sabre.io
Source0:        https://github.com/fruux/sabre-dav/releases/download/%{mainver}/sabredav-%{mainver}.zip
Source1:        %{name}.xml

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{channelname})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(%{channelname})
Requires:       php-pear(%{channelname}/Sabre) >= 1.0.2

Provides:       php-pear(%{pear_name}) = %{version}
Provides:       php-pear(%{channelname}/%{pear_name}) = %{version}

%description
Sabre_HTTP allows for a central interface to deal with Sabre.

%prep
%setup -q -n SabreDAV

cp %{SOURCE1} .
mv lib/Sabre Sabre

# Check version
extver=$(sed -n "/VERSION/{s/.* '//;s/'.*$//;p}" Sabre/HTTP/Version.php)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi

# Check files
touch error.lst
for fic in $(find Sabre/HTTP -type f)
do
  grep $fic %{name}.xml || echo -$fic >> error.lst
done

for fic in $(grep '<file' %{name}.xml | sed -e 's/.*name="//' -e 's/".*//')
do
  [ -f $fic ] || echo +$fic >> error.lst
done

if [ -s error.lst ]; then
  : Error in %{name}.xml
  cat error.lst
  exit 1
fi


%build
# Empty build section, most likely nothing required.

%install
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Sabre/HTTP


%changelog
* Tue Oct 28 2014 Adam Williamson <awilliam@redhat.com> - 1.7.11-1
- new release 1.7.11 (from Sabre 1.7.13 EOL)

* Thu Feb 20 2014 Remi Collet <RPMS@FamilleCollet.com> 1:1.7.10-1
- revert to 1.7

* Tue May  7 2013 Remi Collet <RPMS@FamilleCollet.com> 1.8.5-1
- update to 1.8.1
  use our own package.xml as upstream doesn't use pear anymore

* Mon Nov 12 2012 Remi Collet <RPMS@FamilleCollet.com> 1.6.4-3
- backport for remi repo

* Wed Oct 31 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-3
- specified php required version pointed out by phpci
* Fri Oct 12 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-2
- Fixed Description
* Fri Oct 12 2012 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.4-1
- Version Bump to 1.6.4
- Add necesary deps and Clean up
- Fix documentation path
- remove not needed steps 
- Fixed Description
* Fri Apr 06 2012 Felix Kaechele <heffer@fedoraproject.org> - 1.6.0-1
- initial package
