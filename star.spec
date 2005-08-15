%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif
Summary:  An archiving tool with ACL support
Name: star
Version: 1.5a64
Release: 1
URL: http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/star.html
Source: ftp://ftp.fokus.gmd.de/pub/unix/star/alpha/%{name}-%{version}.tar.gz
Patch0: star-1.5-newMake.patch
Patch2: star-1.5-nofsync.patch
Patch3: star-1.5-davej.patch
Patch4: star-1.5-selinux.patch
License: GPL
Group: Applications/Archiving
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libattr-devel libacl-devel libtool libselinux-devel autoconf213

%description
Star saves many files together into a single tape or disk archive,
and can restore individual files from the archive. Star supports ACL.

%prep
%setup -q -n star-1.5
%patch0 -p1 -b .newMake
%patch2 -p1 -b .nofsync
%patch3 -p1 -b .davej
%if %{WITH_SELINUX}
%patch4 -p1 -b .selinux
%endif


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
	--mandir=%{_mandir} --infodir=%{_infodir}" < /dev/null

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man1
%makeinstall RPM_INSTALLDIR=${RPM_BUILD_ROOT} PARCH=%{_target_cpu} K_ARCH=%{_target_cpu} < /dev/null
rm -rf $RPM_BUILD_ROOT/usr/share/man
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT/usr/share/man

# XXX Nuke unpackaged files.
( cd ${RPM_BUILD_ROOT}
  rm -f .%{_bindir}/mt
  rm -f .%{_bindir}/smt
  rm -f .%{_bindir}/tartest
  rm -f .%{_bindir}/tar
  rm -f .%{_bindir}/gnutar
  rm -f .%{_bindir}/scpio
  rm -f .%{_bindir}/star_fat
  rm -f .%{_bindir}/star_sym
  rm -f .%{_bindir}/suntar
  rm -rf .%{_prefix}/include
  rm -rf .%{_prefix}/lib
  rm -rf .%{_mandir}/man5
  rm -rf .%{_mandir}/man3
  rm -rf .%{_mandir}/man1/{tartest,rmt,gnutar,scpio,smt,suntar}.1*
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
%{_bindir}/spax
%{_mandir}/man1/*.1.gz

%changelog
* Fri Aug 12 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade  1.5a64-1

* Thu Aug 04 2005 Karsten Hopp <karsten@redhat.de> 1.5a54-3
- remove /usr/bin/tar symlink 

* Fri Mar 18 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuilt

* Mon Nov 22 2004 Peter Vrabec <pvrabec@redhat.com>
- upgrade 1.5a54-1 & rebuild

* Mon Oct 25 2004 Peter Vrabec <pvrabec@redhat.com>
- fix dependencie (#123770)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 1.5a25-4
- Fix call to is_selinux_enabled

* Mon Jan 19 2004 Jeff Johnson <jbj@jbj.org> 1.5.a25-3
- fix: (!(x & 1)) rather than (!x & 1) patch.

* Wed Sep 24 2003 Dan Walsh <dwalsh@redhat.com> 1.5a25-2
- turn selinux off

* Tue Sep 16 2003 Dan Walsh <dwalsh@redhat.com> 1.5a25-1.sel
- turn selinux on

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-5
- turn selinux off

* Mon Aug 25 2003 Dan Walsh <dwalsh@redhat.com> 1.5a18-3
- Add SELinux modification to handle setting security context before creation.

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
