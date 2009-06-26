Summary:	Multi-call binary combining many common Unix tools into one executable
Name:		busybox
Version:	1.14.2
Release:	%mkrel 1
Epoch:		1
License:	GPL
Group:		Shells
URL:		http://www.busybox.net/
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2.sign
Source2:	busybox.config
Patch0: busybox-1.12.1-static.patch
Patch12: busybox-1.2.2-ls.patch
Patch14: busybox-1.9.0-msh.patch
Patch16: busybox-1.10.1-hwclock.patch
BuildRequires:	gcc >= 3.3.1-2mdk
BuildRequires:	glibc-static-devel
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
%patch0 -b .static -p1
%patch12 -b .ls -p1
%patch14 -b .msh -p1
%patch16 -b .ia64 -p1

%build
make defconfig
%make CC="gcc"
cp busybox busybox-static
make clean
cp %{_sourcedir}/busybox.config .config
yes "" | make oldconfig
%make
HOSTCC=gcc applets/busybox.mkll > busybox.links

%install
rm -rf %{buildroot}
install -m755 busybox -D %{buildroot}%{_bindir}/busybox
install -m755 busybox-static -D %{buildroot}%{_bindir}/busybox-static

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS README TODO busybox.links
%{_bindir}/*
