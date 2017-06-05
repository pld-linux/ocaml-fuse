#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		modname	Fuse
Summary:	%{modname} binding for OCaml
Summary(pl.UTF-8):	Wiązania %{modname} dla OCamla
Name:		ocaml-fuse
Version:	2.7
Release:	6
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/ocamlfuse/ocamlfuse-%{version}-1.tar.gz
# Source0-md5:	cb9cbe4fafb36ead1b78faaacc26f3e3
URL:		http://sourceforge.net/apps/mediawiki/ocamlfuse/
BuildRequires:	libfuse-devel
BuildRequires:	ocaml >= 3.08
BuildRequires:	ocaml-findlib >= 1.4
BuildRequires:	ocaml-idl-devel >= 1.0.5
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
OcamlFuse is a binding to the high-level part of the fuse library,
allowing you to implement linux filesystems in OCaml. Other operating
systems are not supported, if you think you can help we will be glad
to hear.

The main features of ocamlfuse are:
- Multithreading: each callback runs in a separate ocaml thread, so
  that a slow call can't block the filesystem
- Efficiency: read and write operations use the bigarray library
  achieving very high troughput _ Ease of use: the fusexmp filesystem
  (mimicking bindfs) is 73 lines of code, including in-memory extended
  attributes using a hash table. The hello example is 42 lines of code.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	ocamlfuse binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania ocamlfuse dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
Requires:	libfuse-devel
Requires:	ocaml-idl-devel >= 1.0.5

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -qc
mv ocamlfuse/* .

%build
%{__make} -j1 -C lib \
	byte-code-library \
	%{?with_ocaml_opt:native-code-library} \
	PACKS=camlidl \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
cd lib

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{%{modname},stublibs}
install -p *.cm[ixa]* *.a $RPM_BUILD_ROOT%{_libdir}/ocaml/%{modname}
install -p dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{modname}
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{modname}/META <<EOF
requires = ""
version = "%{version}"
directory = "+%{modname}"
archive(byte) = "%{modname}.cma"
archive(native) = "%{modname}.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE lib/*.mli
%dir %{_libdir}/ocaml/%{modname}
%{_libdir}/ocaml/%{modname}/*.cma
%{_libdir}/ocaml/%{modname}/*.cm[ix]
%{_libdir}/ocaml/%{modname}/libFuse_stubs.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{modname}/Fuse.a
%{_libdir}/ocaml/%{modname}/*.cmxa
%endif
%{_libdir}/ocaml/site-lib/%{modname}
