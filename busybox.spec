%bcond_with		uclibc
%define Werror_cflags	%{nil} 
%define _ssp_cflags	%{nil}

Summary:	Multi-call binary combining many common Unix tools into one executable
Name:		busybox
Version:	1.24.0
Release:	1
Epoch:		1
License:	GPLv2
Group:		Shells
URL:		http://www.busybox.net/
Source0:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1:	http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2.sign
Source2:	busybox-1.23.2-config
Source3:	busybox-1.18.4-minimal-config
Patch1:		busybox-i.15.2-no-march_i386.patch
Patch12:	busybox-1.2.2-ls.patch
# the default behaviour of busybox' pidof implementation is same as for
# 'pidof -x' from the standard implementation, so let's just make it
# ignore -x in stead of returning error
Patch17:	busybox-1.20.2-pidof-x-argument.patch
BuildRequires:	pkgconfig(libtirpc)
%if %{with uclibc}
BuildRequires:	uClibc-static-devel >= 0.9.33.2-3
%define	__cc	%{uclibc_cc}
%define	cflags	%{uclibc_cflags}
%else
%define	__cc	gcc
%define	cflags	%{optflags}
BuildRequires:	glibc-static-devel
%endif

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

%package	static
Group:		Shells
Summary:	Static linked busybox

%description	static
This package contains a static linked busybox.

%package	minimal-static
Group:		Shells
Summary:	Static linked busybox

%description	minimal-static
This package contains a static linked busybox(uClibc).

%package	minimal
Group:		Shells
Summary:	Minimal busybox

%description	minimal
This package contains a minimal busybox.

%prep
%setup -q
%apply_patches

# respect cflags
%if "%(basename %{__cc})" == "clang"
sed -i -e 's:-static-libgcc::' Makefile.flags
# flag cleanup
sed -i -r -e 's:[[:space:]]?-(Werror|Os|falign-(functions|jumps|loops|labels)=1|finline-limit=0|fomit-frame-pointer)\>::g' Makefile.flags
sed -i '/^#error Aborting compilation./d' applets/applets.c
sed -i 's:-Wl,--gc-sections::' Makefile

sed -i \
	-e "/^CROSS_COMPILE/s:=.*:= %{__cc}:" \
	-e "/^AR\>/s:=.*:= %{__ar}:" \
	-e "/^CC\>/s:=.*:= %{__cc}:" \
	-e "/^HOSTCC/s:=.*:= %{__cc}:" \
	Makefile
%endif

%build
%if %{with uclibc}
mkdir -p minimal.static
pushd minimal.static
cp %{SOURCE3}  .config
yes "" | %make oldconfig V=1 KBUILD_SRC=.. -f ../Makefile
%make CC=%{__cc} LDFLAGS="%{ldflags}" V=1 CONFIG_STATIC=y CONFIG_EXTRA_CFLAGS="%{uclibc_cflags}" KBUILD_SRC=.. -f ../Makefile
popd


mkdir -p minimal
pushd minimal
cp %{SOURCE3}  .config
yes "" | %make oldconfig V=1 KBUILD_SRC=.. -f ../Makefile
%make CC=%{__cc} LDFLAGS="%{ldflags}" V=1 CONFIG_STATIC=n CONFIG_EXTRA_CFLAGS="%{uclibc_cflags}" KBUILD_SRC=.. -f ../Makefile
popd
%endif


mkdir -p full.static
pushd full.static
%ifarch aarch64
sed -e 's!CONFIG_FEATURE_HAVE_RPC=y!CONFIG_FEATURE_HAVE_RPC=n!g' > %{SOURCE2}
sed -e 's!CONFIG_FEATURE_INETD_RPC=y!CONFIG_FEATURE_INETD_RPC=n!g' > %{SOURCE2}
%else
cp %{SOURCE2} .config
%endif
yes "" | %make oldconfig V=1 KBUILD_SRC=.. -f ../Makefile
%make CC=%{__cc} LDFLAGS="%{ldflags}" V=1 CONFIG_STATIC=y CONFIG_EXTRA_CFLAGS="%{cflags}" KBUILD_SRC=.. -f ../Makefile
popd

mkdir -p full
pushd full
%ifarch aarch64
sed -e 's!CONFIG_FEATURE_HAVE_RPC=y!CONFIG_FEATURE_HAVE_RPC=n!g' > %{SOURCE2}
sed -e 's!CONFIG_FEATURE_INETD_RPC=y!CONFIG_FEATURE_INETD_RPC=n!g' > %{SOURCE2}
%else
cp %{SOURCE2} .config
%endif
yes "" | %make oldconfig V=1 KBUILD_SRC=.. -f ../Makefile
%make CC=%{__cc} LDFLAGS="%{ldflags}" V=1 CONFIG_STATIC=n CONFIG_EXTRA_CFLAGS="%{cflags}" KBUILD_SRC=.. -f ../Makefile CONFIG_PREFIX=%{buildroot}%{uclibc_root}
popd

%check
# FIXME
%if 0
%make CC=%{__cc} V=1 check
%endif

%install
%if %{with uclibc}
#pushd full
#make install CONFIG_PREFIX=%{buildroot}%{uclibc_root} CC=%{__cc} LDFLAGS="%{ldflags}" V=1 CONFIG_STATIC=n CONFIG_EXTRA_CFLAGS="%{cflags}"
#popd

install -m755 minimal/busybox_unstripped -D %{buildroot}%{uclibc_root}%{_bindir}/busybox.minimal
install -m755 full/busybox_unstripped -D %{buildroot}%{uclibc_root}/bin/busybox
mkdir -p %{buildroot}%{_bindir}
ln -s %{uclibc_root}/bin/busybox %{buildroot}%{_bindir}/busybox
install -m755 minimal.static/busybox_unstripped -D %{buildroot}%{uclibc_root}/bin/busybox.minimal.static
%else
install -m755 full/busybox_unstripped -D %{buildroot}%{_bindir}/busybox
%endif
install -m755 full.static/busybox_unstripped -D %{buildroot}/bin/busybox.static

%files
%doc AUTHORS README TODO
%{_bindir}/busybox
%if %{with uclibc}
%{uclibc_root}/bin/busybox
%endif

%files static
%doc AUTHORS README TODO
/bin/busybox.static

%if %{with uclibc}
%files minimal
%{uclibc_root}%{_bindir}/busybox.minimal

%files minimal-static
%{uclibc_root}/bin/busybox.minimal.static
%endif
