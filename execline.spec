Name:			execline
Version:		1.08
Release:		%mkrel 4

%define _bindir		/bin

Summary:	A light non-interactive scripting language
License:	BSD
Group:		Shells
URL:		http://www.skarnet.org/software/execline/
Source0:	http://www.skarnet.org/software/%{name}/%{name}-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:  skalibs-devel >= 0.40

%description
execline is a very light, non-interactive scripting language, which is 
similar to a shell. Simple shell scripts can be easily rewritten in the 
execline language, improving performance and memory usage. execline was 
designed for use in embedded systems, but works on most Unix flavors.


%prep
%setup -q -n admin


%build

pushd %{name}-%{version}
    echo "gcc %{optflags}" > conf-compile/conf-cc
    echo "gcc %{optflags}" > conf-compile/conf-ld
    echo "/bin/true" >conf-compile/conf-stripbins

    echo "linux-:%{_target_cpu}-:" > src/sys/systype

    echo "%{_includedir}/skalibs" > conf-compile/import
    echo "%{_libdir}/skalibs" >> conf-compile/import

    package/compile
    perl -pi -e 's|\/command|\/bin|g' etc/execline-{startup,shell}
popd


%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

mkdir -p %{buildroot}{%{_sysconfdir},/bin}

pushd %{name}-%{version}
    for i in `cat package/command.exported` ;  do
        install -m 0755 command/$i %{buildroot}/bin/
    done
    install -m 0755 etc/* %{buildroot}%{_sysconfdir}/
popd


%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc %{name}-%{version}/package/CHANGES
%doc %{name}-%{version}/package/README
%doc %{name}-%{version}/doc/*.html
/bin/*
%config(noreplace) %{_sysconfdir}/execline-shell
%config(noreplace) %{_sysconfdir}/execline-startup



%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 1.08-4mdv2011.0
+ Revision: 618247
- the mass rebuild of 2010.0 packages

* Thu Sep 10 2009 Thierry Vignaud <tv@mandriva.org> 1.08-3mdv2010.0
+ Revision: 437503
- rebuild

* Wed Jan 28 2009 Oden Eriksson <oeriksson@mandriva.com> 1.08-2mdv2009.1
+ Revision: 335008
- build against glibc to make it work again

* Wed Jan 28 2009 Oden Eriksson <oeriksson@mandriva.com> 1.08-1mdv2009.1
+ Revision: 334960
- 1.08 (source from freebsd)

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 1.07-2mdv2009.0
+ Revision: 266738
- rebuild early 2009.0 package (before pixel changes)

* Wed May 07 2008 Vincent Danen <vdanen@mandriva.com> 1.07-1mdv2009.0
+ Revision: 202938
- import execline


