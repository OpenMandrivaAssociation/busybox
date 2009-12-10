%bcond_without		uclibc
%define Werror_cflags	%{nil} 
%define _ssp_cflags	%{nil}

Summary:	Multi-call binary combining many common Unix tools into one executable
Name:		busybox
Version:	1.15.2
Release:	%mkrel 2
Epoch:		1
License:	GPL
Group:		Shells
URL:		http://www.busybox.net/
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2.sign
Source2:	busybox-1.15.2-config
Source3:	busybox-1.15.2-minimal-config
#Patch0:	busybox-1.12.1-static.patch
Patch1:		busybox-i.15.2-no-march_i386.patch
Patch12:	busybox-1.2.2-ls.patch
Patch16:	busybox-1.10.1-hwclock.patch
BuildRequires:	gcc >= 3.3.1-2mdk
%if %{with uclibc} 	 
BuildRequires:	uClibc-static-devel >= 0.9.26-5mdk 	 
%define __cc			%{uclibc_cc}
%define	cflags			%{uclibc_cflags}
%else
BuildRequires:	glibc-static-devel
%define	cflags			%{optflags}
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
#%%patch0 -b .static -p1
%patch1 -b .no_march~ -p1
%patch12 -b .ls~ -p1
%patch16 -b .ia64~ -p1

%build
cat %{SOURCE2} |sed \
	-e 's|^.*CONFIG_EXTRA_CFLAGS.*$|CONFIG_EXTRA_CFLAGS="%{cflags} -fno-strict-aliasing"|g' \
	> .config
yes "" | %make oldconfig V=1
%make CC=%{__cc} LDFLAGS="%{ldflags}" V=1
mv busybox_unstripped busybox.full

%if %{with uclibc}
cat %{SOURCE3} |sed \
	-e 's|^.*CONFIG_EXTRA_CFLAGS.*$|CONFIG_EXTRA_CFLAGS="%{cflags} -fno-strict-aliasing"|g' \
	> .config
yes "" | %make oldconfig V=1
%make CC=%{__cc} LDFLAGS="%{ldflags}" V=1
mv busybox_unstripped busybox.minimal
%endif

%check
# FIXME
%if 0
%make CC=%{__cc} V=1 check
%endif

%install
rm -rf %{buildroot}
install -m755 busybox.full -D %{buildroot}%{_bindir}/busybox
%if %{with uclibc}
install -m755 busybox.minimal -D %{buildroot}%{uclibc_root}%{_bindir}/busybox.minimal
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README TODO
%{_bindir}/busybox
%if %{with uclibc}
%{uclibc_root}%{_bindir}/busybox.minimal
%endif
