%define _root_sbindir /sbin
%define _root_libdir /%{_lib}
%define major 2
%define libname %mklibname ext2fs %{major}
%define devname %mklibname ext2fs -d
%define libcom_err %mklibname com_err %{major}
%define devcom_err %mklibname com_err -d
%define libss %mklibname ss %{major}
%define devss %mklibname ss -d

%define git_url git://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git

Summary:	Utilities used for ext2/ext3/ext4 filesystems
Name:		e2fsprogs
Version:	1.45.3
Release:	1
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://e2fsprogs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
Source1:	e3jsize
# (anssi) fix uninitialized variable causing crash without libreadline.so.5;
# submitted as https://sourceforge.net/tracker/?func=detail&aid=2822113&group_id=2406&atid=302406
Patch0:		e2fsprogs-1.41.8-uninitialized.patch
%if %{mdvver} > 3000000
Patch1:		e2fsprogs-1.43.7-fuse3.patch
%endif
BuildRequires:	texinfo
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(uuid)
%if %{mdvver} <= 3000000
BuildRequires:	pkgconfig(fuse)
%else
BuildRequires:	pkgconfig(fuse3)
%endif
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(udev)
Conflicts:	e2fsprogs < 1.42.6-4
Requires:	%{libname} = %{EVRD}
Requires:	%{libcom_err} = %{EVRD}
Requires:	%{libss} = %{EVRD}

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

%prep
%autosetup -p1

rm -f configure
autoconf

# Fix build:
chmod 644 po/*.po

%build
%ifarch %{ix86}
%global ldflags %{ldflags} -fuse-ld=bfd
%endif

%if %{mdvver} > 3000000
%global optflags %{optflags} -I%{_includedir}/fuse3
%endif

%configure \
	--disable-static \
	--enable-elf-shlibs \
	--disable-libblkid \
	--disable-libuuid \
	--disable-fsck \
	--disable-uuidd \
	--enable-symlink-install \
	--disable-e2initrd-helper

%make_build -j1

#%check
#LC_ALL=C make -C check -k || /bin/true

%install
export PATH=/sbin:$PATH

%make_install install-libs root_sbindir=%{_root_sbindir} root_libdir=%{_root_libdir}

%if %{mdvver} <= 3000000
# multiarch policy, alternative is to use <stdint.h>
%multiarch_includes %{buildroot}%{_includedir}/ext2fs/ext2_types.h
%endif

%find_lang %{name}

chmod +x %{buildroot}%{_bindir}/{mk_cmds,compile_et}

install -m 755 %{SOURCE1} %{buildroot}%{_root_sbindir}
ln -f %{buildroot}%{_root_sbindir}/mke2fs %{buildroot}%{_root_sbindir}/mke3fs

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
/lib/systemd/system/e2scrub*
/lib/udev/rules.d/96-e2scrub.rules
%{_root_sbindir}/e2scrub
%{_root_sbindir}/e2scrub_all
%{_libdir}/e2fsprogs
%{_root_sbindir}/badblocks
%{_root_sbindir}/debugfs
%{_root_sbindir}/dumpe2fs
%{_root_sbindir}/e2fsck
%{_root_sbindir}/e2image
%{_root_sbindir}/e2label
%{_root_sbindir}/e2mmpstatus
%{_root_sbindir}/e2undo
%{_root_sbindir}/e3jsize
%{_root_sbindir}/fsck.ext2
%{_root_sbindir}/fsck.ext3
%{_root_sbindir}/fsck.ext4
%{_root_sbindir}/logsave
%{_root_sbindir}/mke2fs
%{_root_sbindir}/mke3fs
%{_root_sbindir}/mkfs.ext2
%{_root_sbindir}/mkfs.ext3
%{_root_sbindir}/mkfs.ext4
%{_root_sbindir}/resize2fs
%{_root_sbindir}/tune2fs
%config(noreplace) %{_sysconfdir}/mke2fs.conf
%{_bindir}/chattr
%{_bindir}/lsattr
%{_mandir}/man1/chattr.1*
%{_mandir}/man1/lsattr.1*
%{_mandir}/man1/fuse2fs.1*
%{_mandir}/man5/e2fsck.conf.5*
%{_mandir}/man5/mke2fs.conf.5*
%{_mandir}/man5/ext?.5*
%{_mandir}/man8/badblocks.8*
%{_mandir}/man8/debugfs.8*
%{_mandir}/man8/dumpe2fs.8*
%{_mandir}/man8/e2freefrag.8*
%{_mandir}/man8/e2fsck.8*
%{_mandir}/man8/e2image.8*
%{_mandir}/man8/e2label.8*
%{_mandir}/man8/e2mmpstatus.8*
%{_mandir}/man8/e2undo.8.*
%{_mandir}/man8/e2scrub*.*
%{_mandir}/man8/e4defrag.8.*
%{_mandir}/man8/filefrag.8*
%{_mandir}/man8/fsck.ext2.8*
%{_mandir}/man8/fsck.ext3.8*
%{_mandir}/man8/fsck.ext4.8.*
%{_mandir}/man8/logsave.8*
%{_mandir}/man8/mke2fs.8*
%{_mandir}/man8/mkfs.ext2.8*
%{_mandir}/man8/mkfs.ext3.8*
%{_mandir}/man8/mkfs.ext4.8.*
%{_mandir}/man8/mklost+found.8*
%{_mandir}/man8/resize2fs.8*
%{_mandir}/man8/tune2fs.8*
%{_mandir}/man8/e4crypt.8*
%{_sbindir}/e2freefrag
%{_sbindir}/e4defrag
%{_sbindir}/filefrag
%{_sbindir}/mklost+found
%{_sbindir}/e4crypt
%{_bindir}/fuse2fs

%files -n %{libname}
%{_root_libdir}/libe2p.so.%{major}*
%{_root_libdir}/libext2fs.so.%{major}*

%files -n %{libcom_err}
%{_root_libdir}/libcom_err.so.%{major}*

%files -n %{devcom_err}
%{_bindir}/compile_et
%{_libdir}/libcom_err.so
%{_datadir}/et
%{_includedir}/et
%{_includedir}/com_err.h
%{_mandir}/man1/compile_et.1*
%{_mandir}/man3/com_err.3*
%{_libdir}/pkgconfig/com_err.pc

%files -n %{libss}
%{_root_libdir}/libss.so.%{major}*

%files -n %{devss}
%{_bindir}/mk_cmds
%{_libdir}/libss.so
%{_datadir}/ss
%{_includedir}/ss
%{_mandir}/man1/mk_cmds.1*
%{_libdir}/pkgconfig/ss.pc

%files -n %{devname}
%doc RELEASE-NOTES
%{_infodir}/libext2fs.info*
%{_libdir}/pkgconfig/e2p.pc
%{_libdir}/pkgconfig/ext2fs.pc
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.so
%{_includedir}/ext2fs
%if %{mdvver} <= 3000000
%dir %{multiarch_includedir}/ext2fs
%{multiarch_includedir}/ext2fs/ext2_types.h
%endif
%dir %{_includedir}/e2p
%{_includedir}/e2p/e2p.h
