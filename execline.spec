Name:			execline
Version:		1.08
Release:		%mkrel 3

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

