%bcond_with	flex_bison_c++
Summary:	A general, open source, retargetable decompiler of native executable files
Summary(pl):	Ogólny, otwarty dekompilator natywnych plików wykonywalnych
Name:		boomerang
Version:	0.0.0.20040708
Release:	0.1
License:	GPL
Group:		Development/Languages
Source0:	%{name}.tar.gz
# Source0-md5:	a9f15806eb670686869f67a06e8a6fbb
Patch0:		%{name}-path.patch
URL:		http://boomerang.sourceforge.net/
%if %{with flex_bison_c++}
BuildRequires:	bison++
BuildRequires:	flex
%endif
BuildRequires:	cppunit-devel
BuildRequires:	expat-devel
BuildRequires:	gc-devel
BuildRequires:	libstdc++-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_chrpath		1

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

%description -l pl
Próba stworzenia prawdziwego dekompilatora przez spo³eczno¶æ otwartego
oprogramowania. Dekompilator przyjmuje na wej¶ciu plik wykonywalny i
próbuje stworzyæ kompilowalny, a nawet zarz±dzalny, plik ¼ród³owy w
jêzyku wy¿szego poziomu wykonuj±cy to samo zadanie. Jest to wiêc
przeciwieñstwo kompilatora, który oczywi¶cie przyjmuje plik ¼ród³owy i
tworzy wykonywalny. Oczywi¶cie dekompilator nie odtworzy oryginalnego
pliku ¼ród³owego; raczej nic z tych rzeczy. Nie ma znaczenia, czy plik
wykonywalny ma symbole czy nie, ani czy zosta³ skompilowany z jakiego¶
konkretnego jêzyka (jednak jêzyki w rodzaju ML, które s± zwykle
interpretowane, nie s± brane pod uwagê).

Intencj± jest stworzenie dekompilatora dla wielu architektur (czyli
takiego, który mo¿e dzia³aæ z ró¿nymi rodzajami wej¶ciowych plików
wykonywalnych z przyzwoitym efektem, np. x86-windows, sparc-solaris
itp.). Bêdzie bardzo modularny, wiêc wiele czê¶ci dekompilatora mo¿e
zostaæ zast±piona eksperymentalnymi modu³ami. Byæ mo¿e stanie siê
interaktywny, jak IDA Pro, poniewa¿ niektóre rzeczy (nie tylko nazwy
zmiennych i komentarze, chocia¿ te s± oczywi¶cie bardzo wa¿ne)
wymagaj± interwencji eksperta.

%prep
%setup -q -n %{name}
%patch0 -p1

%build
find . -type d -name CVS -exec rm -rf "{}" ";" 2> /dev/null || :
find . -type f -name 'Makefile*' -exec sed -i -e 's#^BOOMDIR=.*#BOOMDIR=%{_libdir}/%{name}#g' "{}" ";"

ln -s %{_includedir}/cppunit include/cppunit
%configure

%if ! %{with flex_bison_c++}
%{__make} remote
%endif

%{__make} \
	C="%{__cc} %{rpmcflags} -I%{_includedir}/gc" \
	CC="%{__cxx} %{rpmcflags} -I%{_includedir}/gc"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name}/frontend/machine}

install %{name} $RPM_BUILD_ROOT%{_bindir}
cp -a signatures transformations $RPM_BUILD_ROOT%{_libdir}/%{name}
cp -a frontend/machine/* $RPM_BUILD_ROOT%{_libdir}/%{name}/frontend/machine
find $RPM_BUILD_ROOT%{_libdir}/%{name}/frontend/machine -type f ! -name '*.ssl' -exec rm -f "{}" ";"
cp -a lib $RPM_BUILD_ROOT%{_libdir}/%{name}/lib

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*
%attr(755,root,root) %{_libdir}/%{name}/lib/*.so
%dir %{_libdir}/%{name}/frontend/machine
%dir %{_libdir}/%{name}/frontend/machine/*
%{_libdir}/%{name}/frontend/machine/*/*.ssl
%{_libdir}/%{name}/signatures/*
%{_libdir}/%{name}/transformations/*
