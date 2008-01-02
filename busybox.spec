%ifarch %{sunsparc} x86_64 %{ix86}
%define with_uclibc 1
%else
%define with_uclibc 0
%endif

%{expand: %{?_with_uclibc:         %%global with_uclibc 1}}
%{expand: %{?_without_uclibc:         %%global with_uclibc 0}}

%define name    busybox
%define version 1.6.1
%define release 3

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
Source2:	busybox.config
Patch0: 	http://busybox.net/downloads/fixes-1.6.1/busybox-1.6.1-adduser.patch
Patch1: 	http://busybox.net/downloads/fixes-1.6.1/busybox-1.6.1-init.patch
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
of the utilities you usually find in GNU coreutils, shellutils, etc.
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
%patch0 -p1 -b .adduser
%patch1 -p1 -b .init
cp %{_sourcedir}/busybox.config .config

%build
%if %{with_uclibc}
. uclibc
%make CC="/usr/%{_target_cpu}-linux-uclibc/bin/%{_target_cpu}-uclibc-gcc -static -DKBUILD_NO_NLS" \
      HOSTCC="/usr/%{_target_cpu}-linux-uclibc/bin/%{_target_cpu}-uclibc-gcc -static -DKBUILD_NO_NLS" \
      oldconfig
%make CC="/usr/%{_target_cpu}-linux-uclibc/bin/%{_target_cpu}-uclibc-gcc -static -DKBUILD_NO_NLS" \
      HOSTCC="/usr/%{_target_cpu}-linux-uclibc/bin/%{_target_cpu}-uclibc-gcc -static -DKBUILD_NO_NLS"
%else
%make oldconfig
%make
%endif

%install
rm -rf %{buildroot}
install -m755 busybox -D %{buildroot}%{_bindir}/busybox

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README TODO
%{_bindir}/busybox

