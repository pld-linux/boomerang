Summary:	An attempt at a general, open source, retargetable decompiler of native executable files
Name:		boomerang
Version:	0.0.0.20040707
Release:	0.1
License:	GPL
Group:		Development/Languages
Source0:	%{name}.tar.gz
# Source0-md5:	97d2b1825b3e2d5bcd85df48eb15a45e
URL:		http://boomerang.sourceforge.net/
BuildRequires:	bison++
BuildRequires:	flex
BuildRequires:	gc-devel
BuildRequires:	cppunit-devel
BuildRequires:	expat-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An attempt to develop a real decompiler through the open source
community. A decompiler takes as input an executable file, and
attempts to create a high level, compilable, even maintainable source
file that does the same thing. It is therefore the opposite of a
compiler, which of course takes a source file and makes an executable.
It won't of course recreate the original source file; probably nothing
like it. It does not matter if the executable file has symbols or not,
or was compiled from any particular language. (However, languages like
ML that are usually interpreted are not considered.)

The intent is to create a retargetable decompiler (i.e. one that can
work with different types of input executable files with modest
effort, e.g. X86-windows, sparc-solaris, etc). It will be highly
modular, so that different parts of the decompiler can be replaced
with experimental modules. It is intended to eventually become
interactive, a la IDA Pro, because some things (not just variable
names and comments, though these are obviously very important) require
expert intervention.

%prep
%setup -q -n %{name}

%build
ln -s %{_includedir}/cppunit include/cppunit
%configure

%{__make} \
	C="%{__cc} %{rpmcflags} -I%{_includedir}/gc" \
	CC="%{__cxx} %{rpmcflags} -I%{_includedir}/gc"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/emacs/site-lisp

%{__make} install \
	DESTDIR="$RPM_BUILD_ROOT"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
