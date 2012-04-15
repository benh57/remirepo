Name:           perl-FusionInventory-Agent-Task-NetInventory
Version:        2.1
Release:        1%{?dist}
Summary:        Remote inventory support for FusionInventory Agent
License:        GPLv2+
Group:          Development/Libraries

URL:            http://forge.fusioninventory.org/projects/fusioninventory-agent-task-snmpquery
Source0:        http://search.cpan.org/CPAN/authors/id/F/FU/FUSINV/FusionInventory-Agent-Task-NetInventory-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  perl >= 1:5.8.0
BuildRequires:  perl(ExtUtils::MakeMaker)
# For tests
BuildRequires:  perl(FusionInventory::Agent::Task::NetDiscovery) >= 2.1
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Compile)

Requires:       perl(FusionInventory::Agent::Task::NetDiscovery) >= 2.1
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# upstream have rename from SNMPQuery 1.3 to NetInventory 2.0
Obsoletes:      perl-FusionInventory-Agent-Task-SNMPQuery < 2.0
Provides:       perl-FusionInventory-Agent-Task-SNMPQuery = %{version}-%{release}

%{?perl_default_filter}


%description
This task extracts various information from remote hosts through
SNMP protocol:


%prep
%setup -q -n FusionInventory-Agent-Task-NetInventory-%{version}

%build
perl Makefile.PL \
     PREFIX=%{_prefix} \
     SYSCONFDIR=%{_sysconfdir}/fusioninventory \
     LOCALSTATEDIR=%{_localstatedir}/lib/%{name}

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} $RPM_BUILD_ROOT/*


%check
make test


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc Changes LICENSE README THANKS
%{_datadir}/fusioninventory/lib/FusionInventory/Agent/Task/NetInventory.pm
%{_datadir}/fusioninventory/lib/FusionInventory/Agent/Task/NetInventory
%{_mandir}/man3/*


%changelog
* Sun Apr 15 2012 Remi Collet <remi@fedoraproject.org> - 2.1-1
- rename to perl-FusionInventory-Agent-Task-NetInventory
- update to 2.1 for agent 2.2.0
  http://search.cpan.org/src/FUSINV/FusionInventory-Agent-Task-NetInventory-2.1/Changes

* Wed Mar 30 2011 Remi Collet <Fedora@famillecollet.com> 1.3-1
- update to 1.3
  http://cpansearch.perl.org/src/FUSINV/FusionInventory-Agent-Task-SNMPQuery-1.3/Changes

* Mon Aug 16 2010 Remi Collet <Fedora@famillecollet.com> 1.2-1
- update to 1.2

* Tue May 18 2010 http://blog.famillecollet.com 1.1-1
- Specfile autogenerated by cpanspec 1.78.
- spec cleanup

