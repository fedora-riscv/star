Summary:  An archiving tool with ACL support
Name: star
Version: 1.5a18
Release: 2
URL: http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/star.html
Source: ftp://ftp.fokus.gmd.de/pub/unix/star/alpha/%{name}-%{version}.tar.bz2
Patch: star-1.5-icantusethestandardwayandmademyownmake.patch
Patch1: star-xattr.patch
Patch2: star-nofsync.patch
License: GPL
Group: Applications/Archiving
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libattr-devel libacl-devel libtool

%description
Star saves many files together into a single tape or disk archive,
and can restore individual files from the archive. Star supports ACL.

%prep
%setup -q -n star-1.5
%patch0 -p1
%patch1 -p1 -b .xattr
%patch2 -p1 -b .nofsync
for PLAT in x86_64 ppc64 s390 s390x; do
	for AFILE in gcc cc; do
		[ ! -e RULES/${PLAT}-linux-${AFILE}.rul ] \
		&& ln -s i586-linux-${AFILE}.rul RULES/${PLAT}-linux-${AFILE}.rul
	done
done
cp -f /usr/share/libtool/config.sub conf/config.sub

%build
export CFLAGS="$RPM_OPT_FLAGS"
(cd conf; autoconf-2.13)
make %{?_smp_mflags} PARCH=%{_target_cpu} CPPOPTX="-DNO_FSYNC" \
	K_ARCH=%{_target_cpu} \
	CONFFLAGS="%{_target_platform} --prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} --bindir=%{_bindir} \
	--sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} --includedir=%{_includedir} \
	--libdir=%{_libdir} --libexec=%{_libexecdir} \
	--localstatedir=%{_localstatedir} --sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} --infodir=%{_infodir}"

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1
%makeinstall RPM_INSTALLDIR=${RPM_BUILD_ROOT} PARCH=%{_target_cpu} K_ARCH=%{_target_cpu}
rm -rf $RPM_BUILD_ROOT/usr/share/man
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share/man

# XXX Nuke unpackaged files.
( cd ${RPM_BUILD_ROOT}
  rm -f .%{_bindir}/mt
  rm -f .%{_bindir}/smt
  rm -f .%{_bindir}/tartest
  rm -rf .%{_prefix}/include
  rm -rf .%{_prefix}/lib
  rm -rf .%{_mandir}/man5
  rm -rf .%{_mandir}/man3
  rm -rf .%{_mandir}/man1/{tartest,rmt}.1*
  rm -rf .%{_prefix}/sbin
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README AN* COPYING README.ACL README.crash README.largefiles README.linux
%doc README.otherbugs README.pattern README.posix-2001  README.SSPM STARvsGNUTAR
%doc STATUS.alpha TODO
%{_bindir}/*star
%{_mandir}/man1/star*

%changelog
* Thu Aug 21 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-2
- Fix free_xattr bug

* Wed Jul 16 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-1
- Add SELinux support

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Nov 12 2002 Elliot Lee <sopwith@redhat.com> 1.5a08-3
- Build when uname -m != _target_platform
- Use _smp_mflags
- Build on x86_64

* Mon Nov 11 2002 Jeff Johnson <jbj@redhat.com> 1.5a08-2
- update to 1.5a08.
- build from cvs.

* Wed Jun 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.5a04
- Initial build. Alpha version - it's needed for ACLs.
