Summary:  An archiving tool with ACL support
Name: star
Version: 1.5a04
Release: 1
URL: http://www.fokus.gmd.de/research/cc/glone/employees/joerg.schilling/private/star.html
Source: ftp://ftp.fokus.gmd.de/pub/unix/star/alpha/%{name}-%{version}.tar.bz2
Patch: star-1.5-icantusethestandardwayandmademyownmake.patch
License: GPL
Group: Applications/Archiving
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: libattr-devel libacl-devel

%description
Star saves many files together into a single tape or disk archive,
and can restore individual files from the archive. Star supports ACL.


%prep
%setup -q -n star-1.5
%patch0 -p1

%build
export CFLAGS="$RPM_OPT_FLAGS"
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}
make install RPM_INSTALLDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT/usr/man/* $RPM_BUILD_ROOT/%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README AN* COPYING README.ACL README.crash README.largefiles README.linux
%doc README.otherbugs README.pattern README.posix-2001  README.SSPM STARvsGNUTAR
%doc STATUS.alpha TODO
/usr/bin/star
/usr/bin/ustar
%{_mandir}/man1/star*


%changelog
* Wed Jun 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.5a04
- Initial build. Alpha version - it's needed for ACLs.


