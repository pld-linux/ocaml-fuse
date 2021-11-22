#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	ocamlfuse
Summary:	Fuse binding for OCaml
Summary(pl.UTF-8):	Wiązania Fuse dla OCamla
Name:		ocaml-fuse
Version:	2.7.1
Release:	4
License:	GPL v2
Group:		Libraries
#Source0Download: https://github.com/astrada/ocamlfuse/releases
Source0:	https://github.com/astrada/ocamlfuse/archive/v%{version}_cvs7/ocamlfuse-%{version}-7.tar.gz
# Source0-md5:	a5da871a0983b6723c6b9b735898fe34
Patch0:		no-wrapped.patch
URL:		https://github.com/astrada/ocamlfuse
BuildRequires:	libfuse-devel >= 2.7
BuildRequires:	ocaml >= 1:4.02.3
BuildRequires:	ocaml-dune >= 1.6
BuildRequires:	ocaml-findlib >= 1.4
BuildRequires:	ocaml-idl-devel >= 1.0.5
BuildRequires:	pkgconfig
%requires_eq	ocaml-runtime
Requires:	libfuse >= 2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		debug_package	%{nil}

%description
OcamlFuse is a binding to the high-level part of the fuse library,
allowing you to implement Linux filesystems in OCaml.

The main features of ocamlfuse are:
- Multithreading: each callback runs in a separate ocaml thread, so
  that a slow call can't block the filesystem
- Efficiency: read and write operations use the bigarray library
  achieving very high troughput
- Ease of use: the fusexmp filesystem (mimicking bindfs) is 73 lines
  of code, including in-memory extended attributes using a hash table.
  The hello example is 42 lines of code.

%description -l pl.UTF-8
OcamlFuse to wiązania do wysokopoziomowej części biblioteki fuse,
pozwalające implementować linuksowe systemy plików w OCamlu.

Główne cechy ocamlfuse to:
- wielowątkowość: każde wywołanie zwrotne działa w osobnym wątku
  OCamla, więc powolne wywołanie nie zablokuje systemu plików
- wydajność: operacje odczytu i zapisu wykorzystują bibliotekę
  bigarray, osiągając dużą przepustowość
- łatwość użycia: system plików fusexmp (naśladujący bindfs) ma
  jedynie 73 linie kodu, włącznie z rozszerzonymi atrybutami w
  pamięci, wykorzystującymi tablicę haszującą; przykład "hello
  world" ma 42 linie kodu.

%package devel
Summary:	ocamlfuse binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania ocamlfuse dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
Requires:	libfuse-devel >= 2.7
Requires:	ocaml-idl-devel >= 1.0.5

%description devel
This package contains files needed to develop OCaml programs using
Fuse library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu,
używających biblioteki Fuse.

%prep
%setup -q -n ocamlfuse-2.7.1_cvs7
%patch0 -p1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}/*.ml
# LICENSE is generic GPLv2 text, README.md packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/%{module}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/%{module}/*.cmxs
%endif
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllfuse_stubs.so

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/dune-package
%{_libdir}/ocaml/%{module}/opam
%{_libdir}/ocaml/%{module}/*.cmi
%{_libdir}/ocaml/%{module}/*.cmt
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/*.a
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmx
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
