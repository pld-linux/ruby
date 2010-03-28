#
# Conditional build:
%bcond_without	doc	# skip generating docs (which is time-consuming). Intended for speed up test builds
%bcond_without	emacs	# skip building package with ruby-mode for emacs
%bcond_without	tk	# skip building package with Tk bindings
%bcond_with	onigurma
#
%define		ruby_suffix 18
%define		ruby_ver	1.8
%define		ruby_ridir	%{_datadir}/ri/%{ruby_ver}/system
%define		ruby_rdocdir	%{_datadir}/rdoc
%define		stdlibdoc_version	0.10.1
%define		patchlevel 249
%define		basever 1.8.7
Summary:	Ruby - interpreted scripting language
Summary(ja.UTF-8):	オブジェクト指向言語Rubyインタプリタ
Summary(pl.UTF-8):	Ruby - interpretowany język skryptowy
Summary(pt_BR.UTF-8):	Linguagem de script orientada a objeto
Summary(zh_CN.UTF-8):	ruby - 一种快速高效的面向对象脚本编程语言
Name:		ruby%{ruby_suffix}
Version:	%{basever}.%{patchlevel}
Release:	2
Epoch:		1
License:	The Ruby License
Group:		Development/Languages
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{basever}-p%{patchlevel}.tar.bz2
# Source0-md5:	37200cc956a16996bbfd25bb4068f242
Source1:	http://www.ibiblio.org/pub/languages/ruby/doc/ruby-texi-1.4-en.tar.gz
# Source1-md5:	839fda4af52b5c5c6d21f879f7fc62bf
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/ruby-uguide-981227.tar.gz
# Source2-md5:	24eadcd067278901da9ad70efb146b07
Source3:	http://www.ibiblio.org/pub/languages/ruby/doc/rubyfaq-990927.tar.gz
# Source3-md5:	634c25b14e19925d10af3720d72e8741
Source4:	irb.1
Source5:	http://www.geocities.jp/kosako3/oniguruma/archive/onigd2_5_9.tar.gz
# Source5-md5:	7e4c2b197387232afd9a11378feeb246
Source6:	http://www.ruby-doc.org/download/stdlib/ruby-doc-stdlib-%{stdlibdoc_version}.tgz
# Source6-md5:	5437c281b44e7a4af142d2bd35eba407
Source7:	http://www.ruby-doc.org/download/Ruby-1.8.1_ri_data.zip
# Source7-md5:	96e97cdfa55ed197e0e6c39159394c82
Source8:	erb.1
Source9:	rdoc.1
Source10:	ri.1
Source11:	testrb.1
Source12:	ruby-mode-init.el
Patch0:		ruby-info.patch
Patch1:		ruby-mkmf-shared.patch
Patch2:		ruby-require-rubygems-version.patch
Patch3:		ruby-lib64.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	db-devel
%{?with_emacs:BuildRequires:	emacs}
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	sed >= 4.0
BuildRequires:	texinfo
%if %{with tk}
BuildRequires:	tk-devel
%endif
BuildRequires:	unzip
Requires(post,postun):	/sbin/ldconfig
Provides:	ruby(ver) = %{ruby_ver}
Obsoletes:	rdoc
Obsoletes:	ruby-REXML
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# bleh, some nasty (gcc or ruby) bug still not fixed
# (SEGV or "unexpected break" on miniruby run during build)
%define		specflags_ia64	-O0

# ruby needs frame pointers for correct exception handling
%define		specflags_ia32	-fno-omit-frame-pointer

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text
files and to do system management tasks (as in Perl). It is simple,
straight-forward, extensible, and portable.

This package contains only shared library and ruby interpreter. To get
full-functional ruby environment install ruby-modules package.

%description -l ja.UTF-8
Rubyはシンプルかつ強力なオブジェクト指向スクリプト言語です．Rubyは最初
から純粋なオブジェクト指向言語として設計されていますから，オブジェクト
指向プログラミングを手軽に行う事が出来ます．もちろん通常の手続き型のプ
ログラミングも可能です．

%description -l pl.UTF-8
Ruby to interpretowany język skryptowy, w sam raz dla łatwego i
szybkiego pisania zorientowanych obiektowo programów. Ma wiele funkcji
ułatwiających przetwarzanie plików tekstowych i wykonywanie prac
związanych z zarządzaniem systemu (podobnie jak Perl). Jest prosty,
rozszerzalny i przenośny.

Ten pakiet zawiera tylko bibliotekę dzieloną i interpreter ruby.
Zainstaluj pakiet ruby-modules, jeżeli potrzebujesz w pełni
funkcjonalnego środowiska ruby.

%description -l pt_BR.UTF-8
Ruby é uma linguagem de script interpretada de programação orientada a
objeto. Possui diversas características para processamento de texto. É
simples, extensível e direta.

%package modules
Summary:	Ruby standard modules and utilities
Summary(pl.UTF-8):	Standardowe moduły i narzędzia dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Provides:	ruby-modules(ver) = %{ruby_ver}

%description modules
Ruby standard modules and utilities:
- erb - Tiny eRuby
- rdoc - documentation tool for source code
- irb - interactive Ruby
- ri - Ruby interactive reference
- testrb - automatic runner for Test::Unit of Ruby

%description modules -l pl.UTF-8
Standardowe moduły i narzędzia Ruby:
- erb - mały eRuby
- rdoc - narzędzie do dokumentowania kodu źródłowego
- irb - interaktywny Ruby
- ri - interaktywna dokumentacja Ruby
- testrb - automatyczny runner dla Ruby Test::Unit

%package tk
Summary:	Ruby/Tk bindings
Summary(pl.UTF-8):	Wiązania Ruby/Tk
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description tk
This pachage contains Ruby/Tk bindings.

%description tk -l pl.UTF-8
Ten pakiet zawiera wiązania Ruby/Tk.

%package devel
Summary:	Ruby development libraries
Summary(pl.UTF-8):	Biblioteki programistyczne interpretera języka Ruby
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description devel
Ruby development libraries.

%description devel -l pl.UTF-8
Biblioteki programistyczne interpretera języka Ruby.

%package static
Summary:	Ruby static libraries
Summary(pl.UTF-8):	Biblioteki statyczne Ruby
Group:		Development/Languages
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Ruby static libraries.

%description static -l pl.UTF-8
Biblioteki statyczne Ruby.

%package doc
Summary:	Ruby HTML documentation
Summary(pl.UTF-8):	Dokumentacja HTML do Ruby
Group:		Documentation

%description doc
Ruby HTML documentation: FAQ, guide, core and standard library.

%description doc -l pl.UTF-8
Dokumentacja HTML do Ruby: FAQ, przewodnik, dokumentacja dla core i
stdlib.

%package doc-ri
Summary:	Ruby ri documentation
Summary(pl.UTF-8):	Dokumentacja Ruby w formacie ri
Group:		Documentation
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description doc-ri
Ruby ri documentation.

%description doc-ri -l pl.UTF-8
Dokumentacja Ruby w formacie ri.

%package examples
Summary:	Ruby examples
Summary(pl.UTF-8):	Przykłady dla języka Ruby
Group:		Development/Languages

%description examples
Ruby examples.

%description examples -l pl.UTF-8
Przykłady programów w języku Ruby.

%package emacs-mode
Summary:	Ruby mode and debugger for Emacs
Summary(pl.UTF-8):	Tryb Ruby i debugger dla Emacsa
Group:		Development/Tools
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}
Requires:	emacs-common

%description emacs-mode
Ruby mode and debugger for Emacs.

%description emacs-mode -l pl.UTF-8
Tryb Ruby i debugger dla Emacsa.

%prep
%setup -q -n ruby-%{basever}-p%{patchlevel} -a1 -a2 -a3 -a5 -a6 -a7
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

find -type f '(' -name '*.rb' -o -name '*.cgi' -o -name '*.test' -o -name 'ruby.1' \
	-o -name 'ruby.info*' -o -name '*.html' -o -name '*.tcl' -o -name '*.texi' ')' \
	| xargs %{__sed} -i 's,/usr/local/bin/,%{_bindir}/,'

%build
cp -f /usr/share/automake/config.sub .

%if %{with onigurma}
cd oniguruma
%configure \
	--with-rubydir=..
%{__make} 18
cd ..
%endif

%{__autoconf}
%configure \
	--program-suffix=%{ruby_suffix} \
	--enable-shared \
	--with-default-kcode=utf8 \
	--enable-pthread

%{__make}
%{__make} clean -C ruby-texi-1.4-en
%{__make} info -C ruby-texi-1.4-en

%if %{with doc}
mkdir rdoc

RUBYLIB=".:lib:$(find ext .ext -type d | tr '\n' ':')"
export RUBYLIB
LD_LIBRARY_PATH=$(pwd)
export LD_LIBRARY_PATH

./miniruby bin/rdoc --inline-source --op rdoc/core \
	array.c bignum.c class.c compar.c dir.c dln.c dmyext.c enum.c \
	error.c eval.c file.c gc.c hash.c inits.c io.c lex.c main.c marshal.c \
	math.c numeric.c object.c pack.c parse.c prec.c process.c random.c range.c \
	re.c regex.c ruby.c signal.c sprintf.c st.c string.c struct.c time.c util.c \
	variable.c version.c \
	lib/English.rb lib/abbrev.rb lib/base64.rb lib/benchmark.rb lib/cgi.rb \
	lib/cgi/session.rb lib/complex.rb lib/date.rb lib/fileutils.rb lib/find.rb \
	lib/generator.rb lib/logger.rb lib/matrix.rb lib/observer.rb \
	lib/pathname.rb lib/set.rb lib/shellwords.rb lib/singleton.rb \
	lib/tempfile.rb lib/test/unit.rb lib/thread.rb lib/thwait.rb \
	lib/time.rb lib/yaml.rb

mv ruby-doc-stdlib-%{stdlibdoc_version}/stdlib rdoc/stdlib
mv ri/%{ruby_ver}/site ri/%{ruby_ver}/system

./miniruby bin/rdoc --ri -o ri/%{ruby_ver}/system \
	array.c bignum.c class.c compar.c dir.c dln.c \
	dmyext.c enum.c error.c eval.c file.c gc.c hash.c inits.c io.c lex.c main.c \
	marshal.c math.c numeric.c object.c pack.c parse.c prec.c process.c \
	random.c range.c re.c regex.c ruby.c signal.c sprintf.c st.c string.c \
	struct.c time.c util.c variable.c version.c \
	lib/English.rb lib/abbrev.rb lib/base64.rb lib/benchmark.rb lib/cgi.rb \
	lib/cgi/session.rb lib/complex.rb lib/date.rb lib/fileutils.rb lib/find.rb \
	lib/generator.rb lib/logger.rb lib/matrix.rb lib/observer.rb lib/pathname.rb \
	lib/set.rb lib/shellwords.rb lib/singleton.rb lib/tempfile.rb \
	lib/test/unit.rb lib/thread.rb lib/thwait.rb lib/time.rb lib/yaml.rb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/ruby,%{_infodir},%{_mandir}/man1,%{_examplesdir}/%{name}-%{version},%{ruby_ridir},%{ruby_rdocdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a ruby-texi-1.4-en/ruby.info* $RPM_BUILD_ROOT%{_infodir}
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/irb%{ruby_suffix}.1
cp -a %{SOURCE8} $RPM_BUILD_ROOT%{_mandir}/man1/erb%{ruby_suffix}.1
cp -a %{SOURCE9} $RPM_BUILD_ROOT%{_mandir}/man1/rdoc%{ruby_suffix}.1
cp -a %{SOURCE10} $RPM_BUILD_ROOT%{_mandir}/man1/ri%{ruby_suffix}.1
cp -a %{SOURCE11} $RPM_BUILD_ROOT%{_mandir}/man1/testrb%{ruby_suffix}.1

cp -Rf ruby-uguide guide
cp -Rf rubyfaq faq

%{?with_doc:cp -Rf ri/%{ruby_ver}/system/* $RPM_BUILD_ROOT%{ruby_ridir}}

# ruby emacs mode - borrowed from FC-4
%if %{with emacs}
install -d $RPM_BUILD_ROOT%{_emacs_lispdir}/{ruby-mode,site-start.d}
cp -a misc/*.el $RPM_BUILD_ROOT%{_emacs_lispdir}/ruby-mode
rm -f $RPM_BUILD_ROOT%{_emacs_lispdir}/ruby-mode/rubydb2x.el*
install -p %{SOURCE12} $RPM_BUILD_ROOT%{_emacs_lispdir}/site-start.d
cat << 'EOF' > path.el
(setq load-path (cons "." load-path) byte-compile-warnings nil)
EOF
emacs --no-site-file -q -batch -l path.el -f batch-byte-compile $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode/*.el
rm -f path.el*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}
/sbin/ldconfig

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README README.EXT ChangeLog ToDo
%attr(755,root,root) %{_bindir}/ruby%{ruby_suffix}
%attr(755,root,root) %{_libdir}/libruby%{ruby_suffix}.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libruby%{ruby_suffix}.so.1.8
%{_mandir}/man1/ruby%{ruby_suffix}.1*
%{_infodir}/ruby.info*
%dir %{_libdir}/ruby
%dir %{_libdir}/ruby/%{ruby_ver}
%dir %{_libdir}/ruby/%{ruby_ver}/*-linux*
%dir %{_libdir}/ruby/site_ruby
%dir %{_libdir}/ruby/site_ruby/%{ruby_ver}
%dir %{_libdir}/ruby/site_ruby/%{ruby_ver}/*-linux*
%dir %{_libdir}/ruby/vendor_ruby
%dir %{_libdir}/ruby/vendor_ruby/%{ruby_ver}
%dir %{_libdir}/ruby/vendor_ruby/%{ruby_ver}/*-linux*
%dir %{_datadir}/ruby
%dir %{_datadir}/ri
%dir %{_datadir}/ri/%{ruby_ver}
%dir %{_datadir}/ri/%{ruby_ver}/system
%dir %{ruby_rdocdir}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libruby%{ruby_suffix}.so
%{_libdir}/ruby/%{ruby_ver}/*/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libruby%{ruby_suffix}-static.a

%if %{with tk}
%files tk
%defattr(644,root,root,755)
%{_libdir}/ruby/%{ruby_ver}/tcltk.rb
%{_libdir}/ruby/%{ruby_ver}/tk*.rb
%{_libdir}/ruby/%{ruby_ver}/tk
%{_libdir}/ruby/%{ruby_ver}/tkextlib
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/t*.so
%endif

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erb%{ruby_suffix}
%attr(755,root,root) %{_bindir}/irb%{ruby_suffix}
%attr(755,root,root) %{_bindir}/rdoc%{ruby_suffix}
%attr(755,root,root) %{_bindir}/ri%{ruby_suffix}
%attr(755,root,root) %{_bindir}/testrb%{ruby_suffix}
%{_libdir}/ruby/%{ruby_ver}/bigdecimal
%{_libdir}/ruby/%{ruby_ver}/cgi
%{_libdir}/ruby/%{ruby_ver}/date
%{_libdir}/ruby/%{ruby_ver}/digest
%{_libdir}/ruby/%{ruby_ver}/dl
%{_libdir}/ruby/%{ruby_ver}/drb
%{_libdir}/ruby/%{ruby_ver}/io
%{_libdir}/ruby/%{ruby_ver}/irb
%{_libdir}/ruby/%{ruby_ver}/net
%{_libdir}/ruby/%{ruby_ver}/openssl
%{_libdir}/ruby/%{ruby_ver}/optparse
%{_libdir}/ruby/%{ruby_ver}/racc
%{_libdir}/ruby/%{ruby_ver}/rdoc
%{_libdir}/ruby/%{ruby_ver}/rexml
%{_libdir}/ruby/%{ruby_ver}/rinda
%{_libdir}/ruby/%{ruby_ver}/rss
%{_libdir}/ruby/%{ruby_ver}/runit
%{_libdir}/ruby/%{ruby_ver}/shell
%{_libdir}/ruby/%{ruby_ver}/soap
%{_libdir}/ruby/%{ruby_ver}/test
%{_libdir}/ruby/%{ruby_ver}/uri
%{_libdir}/ruby/%{ruby_ver}/webrick
%{_libdir}/ruby/%{ruby_ver}/wsdl
%{_libdir}/ruby/%{ruby_ver}/xmlrpc
%{_libdir}/ruby/%{ruby_ver}/xsd
%{_libdir}/ruby/%{ruby_ver}/yaml
%{_libdir}/ruby/%{ruby_ver}/[A-Za-s]*.rb
%{_libdir}/ruby/%{ruby_ver}/tempfile.rb
%{_libdir}/ruby/%{ruby_ver}/thread.rb
%{_libdir}/ruby/%{ruby_ver}/thwait.rb
%{_libdir}/ruby/%{ruby_ver}/time.rb
%{_libdir}/ruby/%{ruby_ver}/timeout.rb
%{_libdir}/ruby/%{ruby_ver}/tmpdir.rb
%{_libdir}/ruby/%{ruby_ver}/tracer.rb
%{_libdir}/ruby/%{ruby_ver}/tsort.rb
%{_libdir}/ruby/%{ruby_ver}/[u-z]*.rb
%dir %{_libdir}/ruby/%{ruby_ver}/*-linux*/digest
%dir %{_libdir}/ruby/%{ruby_ver}/*-linux*/io
%dir %{_libdir}/ruby/%{ruby_ver}/*-linux*/racc
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/[a-s]*.so
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/thread.so
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/digest/*.so
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/io/*.so
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/racc/*.so
%attr(755,root,root) %{_libdir}/ruby/%{ruby_ver}/*-linux*/z*.so
%{_libdir}/ruby/%{ruby_ver}/*-linux*/rbconfig.rb
%{_mandir}/man1/erb%{ruby_suffix}.1*
%{_mandir}/man1/irb%{ruby_suffix}.1*
%{_mandir}/man1/rdoc%{ruby_suffix}.1*
%{_mandir}/man1/ri%{ruby_suffix}.1*
%{_mandir}/man1/testrb%{ruby_suffix}.1*

%files doc
%defattr(644,root,root,755)
%doc faq guide
%{?with_doc:%doc rdoc}

%if %{with doc}
%files doc-ri
%defattr(644,root,root,755)
%{_datadir}/ri/%{ruby_ver}/system/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%if %{with emacs}
%files emacs-mode
%defattr(644,root,root,755)
%doc misc/*
%dir %{_emacs_lispdir}/ruby-mode
%{_emacs_lispdir}/ruby-mode/*.elc
%{_emacs_lispdir}/site-start.d/*.el
%endif
