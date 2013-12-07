%define	_root_sbindir	/sbin
%define	_root_libdir	/%{_lib}
%define	major	2
%define libname %mklibname ext2fs %{major}
%define	devname	%mklibname ext2fs -d

%define git_url git://git.kernel.org/pub/scm/fs/ext2/e2fsprogs.git

%bcond_without	uclibc

Summary:	Utilities used for ext2/ext3/ext4 filesystems
Name:		e2fsprogs
Version:	1.42.8
Release:	4
License:	GPLv2
Group:		System/Kernel and hardware
Url:		http://e2fsprogs.sourceforge.net/
Source0:	http://downloads.sourceforge.net/e2fsprogs/%{name}-%{version}.tar.gz
Source1:	e3jsize
# (anssi) fix uninitialized variable causing crash without libreadline.so.5;
# submitted as https://sourceforge.net/tracker/?func=detail&aid=2822113&group_id=2406&atid=302406
Patch0:		e2fsprogs-1.41.8-uninitialized.patch
# (gb) strip references to home build dir
Patch5:		e2fsprogs-1.41.8-strip-me.patch

BuildRequires:	texinfo
BuildRequires:	pkgconfig(blkid)
BuildRequires:	pkgconfig(uuid)
%if %{with uclibc}
BuildRequires:	uClibc-devel >= 0.9.33.2-16
%endif
Conflicts:	e2fsprogs < 1.42.6-4

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

%package -n	uclibc-%{name}
Summary:	Utilities used for ext2/ext3/ext4 filesystems (uClibc linked)
Group:		System/Kernel and hardware

%description -n	uclibc-%{name}
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

%package -n	%{libname}
Summary:	The libraries for Ext2fs
Group:		System/Libraries
Conflicts:	%{_lib}ext2fs2 < 1.42.6-5

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

%package -n	uclibc-%{libname}
Summary:	The libraries for Ext2fs (uClibc linked)
Group:		System/Libraries

%description -n uclibc-%{libname}
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

%package -n	%{devname}
Summary:	The libraries for Ext2fs
Group:		Development/C
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif
Provides:	ext2fs-devel = %{EVRD}

%description -n	%{devname}
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

%prep
%setup -q
%apply_patches

rm -f configure
autoconf

# Fix build:
chmod 644 po/*.po

%build
export CONFIGURE_TOP="$PWD"

%ifarch %{ix86}
%global ldflags %{ldflags} -fuse-ld=bfd
%endif
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--enable-elf-shlibs \
	--disable-libblkid \
	--disable-libuuid \
	--disable-fsck \
	--disable-uuidd \
	--enable-symlink-install \
	--disable-e2initrd-helper
[ -e Makefile ] || cat config.log

%make
%make -C e2fsck
popd
%endif

mkdir -p system
pushd system
%configure2_5x \
	--enable-elf-shlibs \
	--disable-libblkid \
	--disable-libuuid \
	--disable-fsck \
	--disable-uuidd \
	--enable-symlink-install
%make
%make -C e2fsck e2fsck.static
popd

#%check
#LC_ALL=C make -C system check -k || /bin/true

%install
export PATH=/sbin:$PATH

%if %{with uclibc}
%makeinstall_std -C \
	uclibc install-libs \
	root_sbindir=%{uclibc_root}/sbin \
	root_libdir=%{uclibc_root}/%{_lib}
rm -r %{buildroot}%{uclibc_root}%{_libdir}/pkgconfig
for bin in chattr compile_et lsattr mk_cmds; do
	rm %{buildroot}%{uclibc_root}%{_bindir}/$bin
done
%endif

%makeinstall_std -C \
	system install-libs \
	root_sbindir=%{_root_sbindir} \
	root_libdir=%{_root_libdir}

# multiarch policy, alternative is to use <stdint.h>
%multiarch_includes %{buildroot}%{_includedir}/ext2fs/ext2_types.h

%find_lang %{name}

chmod +x %{buildroot}%{_bindir}/{mk_cmds,compile_et}

install -m 755 system/e2fsck/e2fsck.static %{buildroot}%{_root_sbindir}
install -m 755 %{SOURCE1} %{buildroot}%{_root_sbindir}
ln -f %{buildroot}%{_root_sbindir}/mke2fs \
	%{buildroot}%{_root_sbindir}/mke3fs

# fix some files not having write permission by user
chmod u+w -R %{buildroot}

# This should be owned by glibc, not util-linux
rm -rf %{buildroot}%{_datadir}/locale/locale.alias

%files -f %{name}.lang
%doc README
%{_root_sbindir}/badblocks
%{_root_sbindir}/debugfs
%{_root_sbindir}/dumpe2fs
%{_root_sbindir}/e2fsck
%{_root_sbindir}/e2fsck.static
%{_root_sbindir}/e2image
%{_root_sbindir}/e2label
%{_root_sbindir}/e2undo
%{_root_sbindir}/e3jsize
%{_root_sbindir}/fsck.ext2
%{_root_sbindir}/fsck.ext3
%{_root_sbindir}/fsck.ext4
%{_root_sbindir}/fsck.ext4dev
%{_root_sbindir}/logsave
%{_root_sbindir}/mke2fs
%{_root_sbindir}/mke3fs
%{_root_sbindir}/mkfs.ext2
%{_root_sbindir}/mkfs.ext3
%{_root_sbindir}/mkfs.ext4
%{_root_sbindir}/mkfs.ext4dev
%{_root_sbindir}/resize2fs
%{_root_sbindir}/tune2fs
%config(noreplace) %{_sysconfdir}/mke2fs.conf
%{_libexecdir}/e2initrd_helper

%{_bindir}/chattr
%{_bindir}/lsattr
%{_mandir}/man1/chattr.1*
%{_mandir}/man1/lsattr.1*
%{_mandir}/man5/e2fsck.conf.5*
%{_mandir}/man5/mke2fs.conf.5*
%{_mandir}/man8/badblocks.8*
%{_mandir}/man8/debugfs.8*
%{_mandir}/man8/dumpe2fs.8*
%{_mandir}/man8/e2freefrag.8*
%{_mandir}/man8/e2fsck.8*
%{_mandir}/man8/e2image.8*
%{_mandir}/man8/e2label.8*
%{_mandir}/man8/e2undo.8.*
%{_mandir}/man8/e4defrag.8.*
%{_mandir}/man8/filefrag.8*
%{_mandir}/man8/fsck.ext2.8*
%{_mandir}/man8/fsck.ext3.8*
%{_mandir}/man8/fsck.ext4.8.*
%{_mandir}/man8/fsck.ext4dev.8.*
%{_mandir}/man8/logsave.8*
%{_mandir}/man8/mke2fs.8*
%{_mandir}/man8/mkfs.ext2.8*
%{_mandir}/man8/mkfs.ext3.8*
%{_mandir}/man8/mkfs.ext4.8.*
%{_mandir}/man8/mkfs.ext4dev.8.*
%{_mandir}/man8/mklost+found.8*
%{_mandir}/man8/resize2fs.8*
%{_mandir}/man8/tune2fs.8*
%{_sbindir}/e2freefrag
%{_sbindir}/e4defrag
%{_sbindir}/filefrag
%{_sbindir}/mklost+found

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}/sbin/badblocks
%{uclibc_root}/sbin/debugfs
%{uclibc_root}/sbin/dumpe2fs
%{uclibc_root}/sbin/e2fsck
%{uclibc_root}/sbin/e2image
%{uclibc_root}/sbin/e2label
%{uclibc_root}/sbin/e2undo
%{uclibc_root}/sbin/fsck.ext2
%{uclibc_root}/sbin/fsck.ext3
%{uclibc_root}/sbin/fsck.ext4
%{uclibc_root}/sbin/fsck.ext4dev
%{uclibc_root}/sbin/logsave
%{uclibc_root}/sbin/mke2fs
%{uclibc_root}/sbin/mkfs.ext2
%{uclibc_root}/sbin/mkfs.ext3
%{uclibc_root}/sbin/mkfs.ext4
%{uclibc_root}/sbin/mkfs.ext4dev
%{uclibc_root}/sbin/resize2fs
%{uclibc_root}/sbin/tune2fs
%{uclibc_root}%{_sbindir}/e2freefrag
%{uclibc_root}%{_sbindir}/e4defrag
%{uclibc_root}%{_sbindir}/filefrag
%{uclibc_root}%{_sbindir}/mklost+found
%endif

%files -n %{libname}
%doc README
%{_root_libdir}/libcom_err.so.%{major}*
%{_root_libdir}/libe2p.so.%{major}*
%{_root_libdir}/libext2fs.so.%{major}*
%{_root_libdir}/libss.so.%{major}*

%if %{with uclibc}
%files -n uclibc-%{libname}
%doc README
%{uclibc_root}/%{_lib}/libcom_err.so.%{major}*
%{uclibc_root}/%{_lib}/libe2p.so.%{major}*
%{uclibc_root}/%{_lib}/libext2fs.so.%{major}*
%{uclibc_root}/%{_lib}/libss.so.%{major}*
%endif

%files -n %{devname}
%doc RELEASE-NOTES
%{_infodir}/libext2fs.info*
%{_bindir}/compile_et
%{_mandir}/man1/compile_et.1*
%{_bindir}/mk_cmds
%{_mandir}/man1/mk_cmds.1*
%{_libdir}/pkgconfig/*

%{_libdir}/libcom_err.so
%{_libdir}/libe2p.a
%{_libdir}/libe2p.so
%{_libdir}/libext2fs.a
%{_libdir}/libext2fs.so
%{_libdir}/libcom_err.a
%{_libdir}/libquota.a
%{_libdir}/libss.a
%{_libdir}/libss.so

%if %{with uclibc}
%{uclibc_root}%{_libdir}/libcom_err.so
%{uclibc_root}%{_libdir}/libe2p.a
%{uclibc_root}%{_libdir}/libe2p.so
%{uclibc_root}%{_libdir}/libext2fs.a
%{uclibc_root}%{_libdir}/libext2fs.so
%{uclibc_root}%{_libdir}/libcom_err.a
%{uclibc_root}%{_libdir}/libquota.a
%{uclibc_root}%{_libdir}/libss.a
%{uclibc_root}%{_libdir}/libss.so
%endif

%{_datadir}/et
%{_datadir}/ss
%{_includedir}/com_err.h
%{_includedir}/et
%{_includedir}/ext2fs
%dir %{multiarch_includedir}/ext2fs
%{multiarch_includedir}/ext2fs/ext2_types.h
%dir %{_includedir}/quota
%{_includedir}/quota/mkquota.h
%{_includedir}/ss
%dir %{_includedir}/e2p
%{_includedir}/e2p/e2p.h
%{_mandir}/man3/com_err.3*

