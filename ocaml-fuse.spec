#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	ocamlfuse
Summary:	Fuse binding for OCaml
Summary(pl.UTF-8):	Wiązania Fuse dla OCamla
Name:		ocaml-fuse
Version:	2.7.1
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	https://github.com/astrada/ocamlfuse/archive/v%{version}_cvs7/ocamlfuse-%{version}-7.tar.gz
# Source0-md5:	a5da871a0983b6723c6b9b735898fe34
URL:		http://sourceforge.net/apps/mediawiki/ocamlfuse/
BuildRequires:	libfuse-devel
BuildRequires:	ocaml >= 3.08
BuildRequires:	ocaml-dune
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
%setup -q -n ocamlfuse-2.7.1_cvs7

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/ocaml/%{module}/META
%{_libdir}/ocaml/%{module}/dune-package
%{_libdir}/ocaml/%{module}/opam
%{_libdir}/ocaml/%{module}/*.cmi
%{_libdir}/ocaml/%{module}/*.cmt
%{_libdir}/ocaml/%{module}/*.cmti
%{_libdir}/ocaml/%{module}/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE lib/*.mli
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cma
%{_libdir}/ocaml/%{module}/*.cm[ix]
%{_libdir}/ocaml/%{module}/*.a
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
