%define with_uclibc %{?_without_uclibc:0} %{!?_without_uclibc:1}

%ifarch %{sunsparc} x86_64 ppc
%define with_uclibc 0
%endif

%define name	busybox
%define version 1.1.2
%define release	2

Name:		%{name}
Version:	%{version}
Release:	%mkrel %{release}
Epoch:		1
Summary:	Multi-call binary combining many common Unix tools into one executable
License:	GPL
Group:		Shells
URL:		http://www.busybox.net/
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2.sign
Source2:	%{name}-%{version}.config.bz2
BuildRequires:	gcc >= 3.3.1-2mdk
%if %{with_uclibc}
BuildRequires:	uClibc-static-devel >= 0.9.26-5mdk
%else
BuildRequires:	glibc-static-devel
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
BusyBox combines tiny versions of many common UNIX utilities into a
single small executable. It provides minimalist replacements for most
of the utilities you usually find in GNU fileutils, shellutils, etc.
The utilities in BusyBox generally have fewer options than their
full-featured GNU cousins; however, the options that are included provide
the expected functionality and behave very much like their GNU counterparts.
BusyBox provides a fairly complete POSIX environment for any small or
embedded system.

BusyBox has been written with size-optimization and limited resources in
mind. It is also extremely modular so you can easily include or exclude
commands (or features) at compile time. This makes it easy to customize
your embedded systems. To create a working system, just add /dev, /etc,
and a kernel.

%prep
%setup -q
bzcat %{SOURCE2} > .config
perl -pi -e "s#-march=i386#-march=i586 -mtune=pentiumpro#g" Rules.mak

%build
%make oldconfig
%make dep
%if %{with_uclibc}
. uclibc
%endif
%make

%install
rm -rf $RPM_BUILD_ROOT
install -m755 busybox -D $RPM_BUILD_ROOT%{_bindir}/busybox
install -m644 docs/BusyBox.1 -D $RPM_BUILD_ROOT%{_mandir}/man1/busybox.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS INSTALL README TODO docs/BusyBox.txt
%{_bindir}/busybox
%{_mandir}/man1/busybox.1*

