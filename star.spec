%if %{?WITH_SELINUX:0}%{!?WITH_SELINUX:1}
%define WITH_SELINUX 1
%endif
Summary:  An archiving tool with ACL support
Name: star
Version: 1.5a84
Release: 3%{?dist}
URL: http://cdrecord.berlios.de/old/private/star.html
Source: ftp://ftp.berlios.de/pub/star/alpha/%{name}-%{version}.tar.bz2
Patch1: star-1.5-newMake.patch
Patch2: star-1.5-selinux.patch
Patch3: star-1.5-changewarnSegv.patch
License: CDDL
Group: Applications/Archiving
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libattr-devel libacl-devel libtool libselinux-devel 
BuildRequires: e2fsprogs-devel gawk
 
%description
Star saves many files together into a single tape or disk archive,
and can restore individual files from the archive. Star supports ACL.

%prep
%setup -q -n star-1.5
%patch1 -p1 -b .newMake
%if %{WITH_SELINUX}
%patch2 -p1 -b .selinux
%endif
%patch3 -p1 -b .changewarnSegv

for PLAT in %{arm} x86_64 ppc64 s390 s390x; do
        for AFILE in gcc cc; do
                [ ! -e RULES/${PLAT}-linux-${AFILE}.rul ] \
                && ln -s i586-linux-${AFILE}.rul RULES/${PLAT}-linux-${AFILE}.rul
        done
done

%build
export COPTOPT="$RPM_OPT_FLAGS"
export MAKEPROG=gmake
# Autoconfiscate
(cd conf; AC_MACRODIR=. AWK=gawk ./autoconf)
# Disable fat binary
(cd star; rm Makefile; cp all.mk Makefile)

#make %{?_smp_mflags} PARCH=%{_target_cpu} CPPOPTX="-DNO_FSYNC" \
make %{?_smp_mflags} PARCH=%{_target_cpu} \
	COPTX='-O0' \
	K_ARCH=%{_target_cpu} \
	CONFFLAGS="%{_target_platform} --prefix=%{_prefix} \
	--exec-prefix=%{_exec_prefix} --bindir=%{_bindir} \
	--sbindir=%{_sbindir} --sysconfdir=%{_sysconfdir} \
	--datadir=%{_datadir} --includedir=%{_includedir} \
	--libdir=%{_libdir} --libexec=%{_libexecdir} \
	--localstatedir=%{_localstatedir} --sharedstatedir=%{_sharedstatedir} \
	--mandir=%{_mandir} --infodir=%{_infodir}" < /dev/null

%install
export MAKEPROG=gmake
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man1
%makeinstall RPM_INSTALLDIR=${RPM_BUILD_ROOT} PARCH=%{_target_cpu} K_ARCH=%{_target_cpu} < /dev/null
rm -rf $RPM_BUILD_ROOT/usr/share/man
rm -rf $RPM_BUILD_ROOT/usr/share/doc/rmt
mv $RPM_BUILD_ROOT/usr/man $RPM_BUILD_ROOT%{_mandir}

# XXX Nuke unpackaged files.
( cd ${RPM_BUILD_ROOT}
  rm -f .%{_prefix}%{_sysconfdir}/default/rmt
  rm -f .%{_bindir}/mt
  rm -f .%{_bindir}/smt
  rm -f .%{_bindir}/tartest
  rm -f .%{_bindir}/tar
  rm -f .%{_bindir}/gnutar
  rm -f .%{_bindir}/scpio
  rm -f .%{_bindir}/star_fat
  rm -f .%{_bindir}/star_sym
  rm -f .%{_bindir}/suntar
  rm -rf .%{_prefix}%{_sysconfdir}
  rm -rf .%{_prefix}/include
  rm -rf .%{_prefix}/lib
  rm -rf .%{_mandir}/man5
  rm -rf .%{_mandir}/man3
  rm -rf .%{_mandir}/man1/{tartest,rmt,gnutar,scpio,smt,suntar,match}.1*
  rm -rf .%{_sbindir}
)

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README AN* COPYING CDDL.Schily.txt README.SSPM STATUS.alpha TODO
%{_bindir}/star
%{_bindir}/ustar
%{_bindir}/spax
%{_mandir}/man1/star.1*
%{_mandir}/man1/spax.1*

%changelog
* Fri Aug 31 2007 Dan Kopecek <dkopecek@redhat.com> 1.5a84-3
- added -O0 to COPTX (CFLAGS) (see #255261)

* Mon Aug 27 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a84-2
- fix segfault of data-change-warn option (#255261), 
  patch from dkopecek@redhat.com

* Fri Aug 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a84-1
- new upstream release with CVE-2007-4134 fix

* Sun Jun 24 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a76-3
- build star on ARM platforms (#245465)

* Mon Jan 29 2007 Peter Vrabec <pvrabec@redhat.com> 1.5a76-2
- fix buildreq. and rebuild

* Thu Jan 18 2007 Jan Cholasta <grubber.x@gmail.com> 1.5a76-1 
- upgrade

* Tue Aug 08 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a75-1
- upgrade

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.5a74-3.1
- rebuild

* Tue Jun 13 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a74-3
- use autoconf provided by star

* Fri Jun 02 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a74-2
- update tarball

* Mon Apr 24 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a74-1
- upgrade

* Wed Mar 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a73-1
- upgrade

* Wed Mar 01 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a72-1
- upgrade

* Wed Feb 22 2006 Peter Vrabec <pvrabec@redhat.com> 1.5a71-1
- upgrade

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 08 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a69-1
- upgrade

* Mon Oct 10 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a68-1
- upgrade

* Thu Sep 22 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a67-1
- upgrade

* Fri Aug 26 2005 Peter Vrabec <pvrabec@redhat.com> 1.5a65-1
- upgrade 1.5a65-1 made by Horst H. von Brand <vonbrand@inf.utfsm.cl>
- Source URL changed, no homepage now
- License changed from GPL to CDDL 1.0
- Define MAKEPROG=gmake like the Gmake.linux script does
- Disable fat binary as per star/Makefile, update star-1.5-selinux.patch for
  the various *.mk files used in that case
- Axe /usr/share/man/man1/match.1*, /usr/etc/default/rmt too
- Explicit listing in %files, allow for compressed or plain manpages

* Fri Aug 26 2005 Peter Vrabec <pvrabec@redhat.com>
- do not remove star_fat

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
