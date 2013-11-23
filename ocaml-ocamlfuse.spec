# disable debug - not useful?
%define debug_package %{nil}

#
# Conditional build:
%bcond_with	opt		# build opt

Summary:	ocamlfuse binding for OCaml
Summary(pl.UTF-8):	Wiązania ocamlfuse dla OCamla
Name:		ocaml-ocamlfuse
Version:	2.7
Release:	1
License:	GPL v2
Group:		Libraries
Source0:	http://downloads.sourceforge.net/ocamlfuse/ocamlfuse-%{version}-1.tar.gz
# Source0-md5:	cb9cbe4fafb36ead1b78faaacc26f3e3
URL:		http://sourceforge.net/apps/mediawiki/ocamlfuse/
BuildRequires:	libfuse-devel
BuildRequires:	ocaml >= 3.08
BuildRequires:	ocaml-camlidl >= 1.0.5
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
%{__make} all %{?with_opt:opt} -C lib \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
cd lib

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{ocamlfuse,stublibs}
install *.cm[ixa]* *.a dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/ocamlfuse
install dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlfuse
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/ocamlfuse/META <<EOF
requires = ""
version = "%{version}"
directory = "+ocamlfuse"
archive(byte) = "ocamlfuse.cma"
archive(native) = "ocamlfuse.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/ocaml/stublibs/*.so
%dir %{_libdir}/ocaml/ocamlfuse
%attr(755,root,root) %{_libdir}/ocaml/ocamlfuse/dll*_stubs.so

%files devel
%defattr(644,root,root,755)
%doc LICENSE lib/*.mli
%dir %{_libdir}/ocaml/ocamlfuse
%{_libdir}/ocaml/ocamlfuse/*.cm[ixa]*
%{_libdir}/ocaml/ocamlfuse/*.a
%{_libdir}/ocaml/site-lib/ocamlfuse
