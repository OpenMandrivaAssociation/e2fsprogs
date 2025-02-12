%define major 2
%define libname %mklibname ext2fs %{major}
%define devname %mklibname ext2fs -d
%define libcom_err %mklibname com_err %{major}
%define devcom_err %mklibname com_err -d
%define libss %mklibname ss %{major}
%define devss %mklibname ss -d
%define git_url git://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git

# libcom_err is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%define lib32name libext2fs%{major}
%define dev32name libext2fs-devel
%define lib32com_err libcom_err%{major}
%define dev32com_err libcom_err-devel
%define lib32ss libss%{major}
%define dev32ss libss-devel

Summary:	Utilities used for ext2/ext3/ext4 filesystems
Name:		e2fsprogs
Version:	1.47.2
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
Url:		https://e2fsprogs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
Source1:	e3jsize
# (anssi) fix uninitialized variable causing crash without libreadline.so.5;
# submitted as https://sourceforge.net/tracker/?func=detail&aid=2822113&group_id=2406&atid=302406
Patch0:		e2fsprogs-1.41.8-uninitialized.patch
BuildRequires:	texinfo
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(fuse3)
BuildRequires:	systemd-macros
BuildRequires:	pkgconfig(udev)
Conflicts:	e2fsprogs < 1.42.6-4
Requires:	%{libname} = %{EVRD}
Requires:	%{libcom_err} = %{EVRD}
Requires:	%{libss} = %{EVRD}
%if %{with compat32}
BuildRequires:	libc6
BuildRequires:	devel(libblkid)
BuildRequires:	devel(libuuid)
%endif

%description
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in ext2, ext3,
and ext4 filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters), resize2fs to grow and shrink
unmounted filesystems, and most of the other core ext2fs filesystem
utilities.

%package -n %{libname}
Summary:	The libraries for Ext2fs
Group:		System/Libraries
Conflicts:	%{_lib}ext2fs2 < 1.42.6-5
Requires:	%{libcom_err} = %{EVRD}

%description -n %{libname}
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in ext2, ext3,
and ext4 filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters), resize2fs to grow and shrink
unmounted filesystems, and most of the other core ext2fs filesystem
utilities.

This package contains the shared libraries.

%package -n %{devname}
Summary:	The libraries for Ext2fs
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%{devcom_err} = %{EVRD}
Provides:	ext2fs-devel = %{EVRD}

%description -n %{devname}
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in ext2, ext3,
and ext4 filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters), resize2fs to grow and shrink
unmounted filesystems, and most of the other core ext2fs filesystem
utilities.

You should install %{libname} to use tools that compile with ext2fs
features.

%package -n %{libcom_err}
Summary:	Common error description library
Group:		System/Libraries
Conflicts:	%{libname} < 1.44.1-2

%description -n %{libcom_err}
This is the common error description library, part of e2fsprogs.
libcom_err is an attempt to present a common error-handling mechanism.

%package -n %{devcom_err}
Summary:	Headers and development files for %{libcom_err}
Group:		Development/C
Requires:	%{libcom_err} = %{EVRD}
Conflicts:	%{devname} < 1.44.1-2

%description -n %{devcom_err}
This is the common error description development library and headers,
part of e2fsprogs.  It contains the compile_et command, used
to convert a table listing error-code names and associated messages
messages into a C source file suitable for use with the library.

libcom_err is an attempt to present a common error-handling mechanism.

%package -n %{libss}
Summary:	Command line interface parsing library
Group:		System/Libraries
Requires:	%{libcom_err} = %{EVRD}
Conflicts:	%{libname} < 1.44.1-2

%description -n %{libss}
This is libss, a command line interface parsing library, part of e2fsprogs.

This package includes a tool that parses a command table to generate
a simple command-line interface parser, the include files needed to
compile and use it.

It was originally inspired by the Multics SubSystem library.

%package -n %{devss}
Summary:	Headers and development files for %{libss}
Group:		Development/C
Requires:	%{libss} = %{EVRD}
Conflicts:	%{devname} < 1.44.1-2

%description -n %{devss}
This is the command line interface parsing (libss) development library
and headers, part of e2fsprogs.  It contains the mk_cmds command, which
parses a command table to generate a simple command-line interface parser.

It was originally inspired by the Multics SubSystem library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	The libraries for Ext2fs (32-bit)
Group:		System/Libraries
Requires:	%{lib32com_err} = %{EVRD}

%description -n %{lib32name}
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in ext2, ext3,
and ext4 filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters), resize2fs to grow and shrink
unmounted filesystems, and most of the other core ext2fs filesystem
utilities.

This package contains the shared libraries.

%package -n %{dev32name}
Summary:	The libraries for Ext2fs (32-bit)
Group:		Development/C
Requires:	%{lib32name} = %{EVRD}
Requires:	%{dev32com_err} = %{EVRD}
Requires:	%{devname} = %{EVRD}

%description -n %{dev32name}
The e2fsprogs package contains a number of utilities for creating,
checking, modifying and correcting any inconsistencies in ext2, ext3,
and ext4 filesystems.  E2fsprogs contains e2fsck (used to repair
filesystem inconsistencies after an unclean shutdown), mke2fs (used to
initialize a partition to contain an empty ext2 filesystem), debugfs
(used to examine the internal structure of a filesystem, to manually
repair a corrupted filesystem or to create test cases for e2fsck), tune2fs
(used to modify filesystem parameters), resize2fs to grow and shrink
unmounted filesystems, and most of the other core ext2fs filesystem
utilities.

You should install %{lib32name} to use tools that compile with ext2fs
features.

%package -n %{lib32com_err}
Summary:	Common error description library (32-bit)
Group:		System/Libraries

%description -n %{lib32com_err}
This is the common error description library, part of e2fsprogs.
libcom_err is an attempt to present a common error-handling mechanism.

%package -n %{dev32com_err}
Summary:	Headers and development files for %{libcom_err} (32-bit)
Group:		Development/C
Requires:	%{lib32com_err} = %{EVRD}

%description -n %{dev32com_err}
This is the common error description development library and headers,
part of e2fsprogs.  It contains the compile_et command, used
to convert a table listing error-code names and associated messages
messages into a C source file suitable for use with the library.

libcom_err is an attempt to present a common error-handling mechanism.

%package -n %{lib32ss}
Summary:	Command line interface parsing library (32-bit)
Group:		System/Libraries
Requires:	%{lib32com_err} = %{EVRD}

%description -n %{lib32ss}
This is libss, a command line interface parsing library, part of e2fsprogs.

This package includes a tool that parses a command table to generate
a simple command-line interface parser, the include files needed to
compile and use it.

It was originally inspired by the Multics SubSystem library.

%package -n %{dev32ss}
Summary:	Headers and development files for %{lib32ss} (32-bit)
Group:		Development/C
Requires:	%{lib32ss} = %{EVRD}

%description -n %{dev32ss}
This is the command line interface parsing (libss) development library
and headers, part of e2fsprogs.  It contains the mk_cmds command, which
parses a command table to generate a simple command-line interface parser.

It was originally inspired by the Multics SubSystem library.
%endif

%prep
%autosetup -p1

rm -f configure
autoconf

# Fix build:
chmod 644 po/*.po

%build
%ifarch %{ix86}
%global buil_ldflags %{build_ldflags} -fuse-ld=bfd
%endif

%if %{cross_compiling}
%global optflags %{optflags} -Oz -I%{_prefix}/%{_target_platform}/include/fuse3
%else
%global optflags %{optflags} -Oz -I%{_includedir}/fuse3
%endif

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir build32
cd build32
%configure32 \
	--enable-elf-shlibs \
	--disable-libblkid \
	--disable-libuuid \
	--disable-fsck \
	--disable-uuidd \
	--enable-symlink-install \
	--disable-e2initrd-helper \
	--with-systemd-unit-dir=%{_unitdir}
cd ..
%make_build -j1 -C build32
%endif

mkdir build
cd build
%configure \
	--enable-elf-shlibs \
	--disable-libblkid \
	--disable-libuuid \
	--disable-fsck \
	--disable-uuidd \
	--enable-symlink-install \
	--disable-e2initrd-helper \
	--with-systemd-unit-dir=%{_unitdir}
cd ..

%make_build -j1 -C build

#%check
#LC_ALL=C make -C check -k || /bin/true

%install
export PATH=/sbin:$PATH

%if %{with compat32}
%make_install -C build32 install-libs root_sbindir=%{_sbindir} root_libdir=%{_prefix}/lib
rm -rf %{buildroot}%{_prefix}/lib/lib{com_err,e2p,ext2fs,ss}.a %{buildroot}%{_prefix}/lib/e2fsprogs %{buildroot}%{_sbindir}/*
%endif
%make_install -C build install-libs root_sbindir=%{_sbindir} root_libdir=%{_libdir}

%find_lang %{name}

chmod +x %{buildroot}%{_bindir}/{mk_cmds,compile_et}

install -m 755 %{SOURCE1} %{buildroot}%{_sbindir}
ln -f %{buildroot}%{_sbindir}/mke2fs %{buildroot}%{_sbindir}/mke3fs

# fix some files not having write permission by user
chmod u+w -R %{buildroot}

# This should be owned by glibc, not util-linux
rm -rf %{buildroot}%{_datadir}/locale/locale.alias

# remove static libraries with a shared counterpart
rm %{buildroot}%{_libdir}/lib{com_err,e2p,ext2fs,ss}.a

# We don't need the cron job, use a systemd timer if necessary
rm -rf %{buildroot}%{_sysconfdir}/cron.d

%files -f %{name}.lang
%doc README
%{_sysconfdir}/e2scrub.conf
%{_unitdir}/e2scrub*
%{_udevrulesdir}/64-ext4.rules
%{_udevrulesdir}/96-e2scrub.rules
%{_sbindir}/e2scrub
%{_sbindir}/e2scrub_all
%{_libexecdir}/e2fsprogs
%{_sbindir}/badblocks
%{_sbindir}/debugfs
%{_sbindir}/dumpe2fs
%{_sbindir}/e2fsck
%{_sbindir}/e2image
%{_sbindir}/e2label
%{_sbindir}/e2mmpstatus
%{_sbindir}/e2undo
%{_sbindir}/e3jsize
%{_sbindir}/fsck.ext2
%{_sbindir}/fsck.ext3
%{_sbindir}/fsck.ext4
%{_sbindir}/logsave
%{_sbindir}/mke2fs
%{_sbindir}/mke3fs
%{_sbindir}/mkfs.ext2
%{_sbindir}/mkfs.ext3
%{_sbindir}/mkfs.ext4
%{_sbindir}/resize2fs
%{_sbindir}/tune2fs
%config(noreplace) %{_sysconfdir}/mke2fs.conf
%{_bindir}/chattr
%{_bindir}/lsattr
%doc %{_mandir}/man1/chattr.1*
%doc %{_mandir}/man1/lsattr.1*
%doc %{_mandir}/man1/fuse2fs.1*
%doc %{_mandir}/man5/e2fsck.conf.5*
%doc %{_mandir}/man5/mke2fs.conf.5*
%doc %{_mandir}/man5/ext?.5*
%doc %{_mandir}/man8/badblocks.8*
%doc %{_mandir}/man8/debugfs.8*
%doc %{_mandir}/man8/dumpe2fs.8*
%doc %{_mandir}/man8/e2freefrag.8*
%doc %{_mandir}/man8/e2fsck.8*
%doc %{_mandir}/man8/e2image.8*
%doc %{_mandir}/man8/e2label.8*
%doc %{_mandir}/man8/e2mmpstatus.8*
%doc %{_mandir}/man8/e2undo.8.*
%doc %{_mandir}/man8/e2scrub*.*
%doc %{_mandir}/man8/e4defrag.8.*
%doc %{_mandir}/man8/filefrag.8*
%doc %{_mandir}/man8/fsck.ext2.8*
%doc %{_mandir}/man8/fsck.ext3.8*
%doc %{_mandir}/man8/fsck.ext4.8.*
%doc %{_mandir}/man8/logsave.8*
%doc %{_mandir}/man8/mke2fs.8*
%doc %{_mandir}/man8/mkfs.ext2.8*
%doc %{_mandir}/man8/mkfs.ext3.8*
%doc %{_mandir}/man8/mkfs.ext4.8.*
%doc %{_mandir}/man8/mklost+found.8*
%doc %{_mandir}/man8/resize2fs.8*
%doc %{_mandir}/man8/tune2fs.8*
%doc %{_mandir}/man8/e4crypt.8*
%{_sbindir}/e2freefrag
%{_sbindir}/e4defrag
%{_sbindir}/filefrag
%{_sbindir}/mklost+found
%{_sbindir}/e4crypt
%{_bindir}/fuse2fs

%files -n %{libname}
%{_libdir}/libe2p.so.%{major}*
%{_libdir}/libext2fs.so.%{major}*

%files -n %{libcom_err}
%{_libdir}/libcom_err.so.%{major}*

%files -n %{devcom_err}
%{_bindir}/compile_et
%{_libdir}/libcom_err.so
%{_datadir}/et
%{_includedir}/et
%{_includedir}/com_err.h
%doc %{_mandir}/man1/compile_et.1*
%doc %{_mandir}/man3/com_err.3*
%{_libdir}/pkgconfig/com_err.pc

%files -n %{libss}
%{_libdir}/libss.so.%{major}*

%files -n %{devss}
%{_bindir}/mk_cmds
%{_libdir}/libss.so
%{_datadir}/ss
%{_includedir}/ss
%doc %{_mandir}/man1/mk_cmds.1*
%{_libdir}/pkgconfig/ss.pc

%files -n %{devname}
%doc RELEASE-NOTES
%doc %{_infodir}/libext2fs.info*
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/pkgconfig/ext2fs.pc
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.so
%{_includedir}/ext2fs
%dir %{_includedir}/e2p
%{_includedir}/e2p/e2p.h

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libe2p.so.%{major}*
%{_prefix}/lib/libext2fs.so.%{major}*

%files -n %{lib32com_err}
%{_prefix}/lib/libcom_err.so.%{major}*

%files -n %{dev32com_err}
%{_prefix}/lib/libcom_err.so
%{_prefix}/lib/pkgconfig/com_err.pc

%files -n %{lib32ss}
%{_prefix}/lib/libss.so.%{major}*

%files -n %{dev32ss}
%{_prefix}/lib/libss.so
%{_prefix}/lib/pkgconfig/ss.pc

%files -n %{dev32name}
%{_prefix}/lib/pkgconfig/e2p.pc
%{_prefix}/lib/pkgconfig/ext2fs.pc
%{_prefix}/lib/libe2p.so
%{_prefix}/lib/libext2fs.so
%endif
