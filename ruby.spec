#
# Conditional build:
%bcond_without	emacs	# skip building package with ruby-mode for emacs
#
%define		ruby_ver	1.8
%define		ruby_ridir	%{_datadir}/ri/%{ruby_ver}/system
Summary:	Ruby - interpreted scripting language
Summary(ja):	¥ª¥Ö¥¸¥§¥¯¥È»Ø¸þ¸À¸ìRuby¥¤¥ó¥¿¥×¥ê¥¿
Summary(pl):	Ruby - interpretowany jêzyk skryptowy
Summary(pt_BR):	Linguagem de script orientada a objeto
Summary(zh_CN):	ruby - Ò»ÖÖ¿ìËÙ¸ßÐ§µÄÃæÏò¶ÔÏó½Å±¾±à³ÌÓïÑÔ
Name:		ruby
Version:	1.8.5
Release:	1
Epoch:		1
License:	The Ruby License
Group:		Development/Languages
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/%{name}-%{version}.tar.gz
# Source0-md5:	3fbb02294a8ca33d4684055adba5ed6f
Source1:	http://www.ibiblio.org/pub/languages/ruby/doc/%{name}-texi-1.4-en.tar.gz
# Source1-md5:	839fda4af52b5c5c6d21f879f7fc62bf
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/%{name}-uguide-981227.tar.gz
# Source2-md5:	24eadcd067278901da9ad70efb146b07
Source3:	http://www.ibiblio.org/pub/languages/ruby/doc/%{name}faq-990927.tar.gz
# Source3-md5:	634c25b14e19925d10af3720d72e8741
Source4:	irb.1
Source5:	http://www.geocities.jp/kosako3/oniguruma/archive/onigd2_5_7.tar.gz
# Source5-md5:	dcaa0b3608990791a5348e94b2f427d5
%define stdlibdoc_version	0.10.1
Source6:	http://www.ruby-doc.org/download/stdlib/%{name}-doc-stdlib-%{stdlibdoc_version}.tgz
# Source6-md5:	5437c281b44e7a4af142d2bd35eba407
Source7:	http://www.ruby-doc.org/download/Ruby-1.8.1_ri_data.zip
# Source7-md5:	96e97cdfa55ed197e0e6c39159394c82
Source8:	erb.1
Source9:	rdoc.1
Source10:	ri.1
Source11:	testrb.1
Source12:	%{name}-mode-init.el
Patch0:		%{name}-info.patch
Patch1:		%{name}-LIB_PREFIX.patch
Patch2:		%{name}-mkmf-shared.patch
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
BuildRequires:	tk-devel
BuildRequires:	unzip
Requires(post,postun):	/sbin/ldconfig
Provides:	ruby(ver) = %{ruby_ver}
Obsoletes:	rdoc
Obsoletes:	ruby-REXML
Obsoletes:	ruby-doc < 1.8.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	%{_prefix}/lib

# bleh, some nasty (gcc or ruby) bug still not fixed
# (SEGV or "unexpected break" on miniruby run during build)
%define		specflags_ia64	-O0

# ruby needs frame pointers for correct exception handling
%define		specflags	-fno-omit-frame-pointer

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text
files and to do system management tasks (as in Perl). It is simple,
straight-forward, extensible, and portable.

This package contains only shared library and ruby interpreter. To get
full-functional ruby environment install ruby-modules package.

%description -l ja
Ruby¤Ï¥·¥ó¥×¥ë¤«¤Ä¶¯ÎÏ¤Ê¥ª¥Ö¥¸¥§¥¯¥È»Ø¸þ¥¹¥¯¥ê¥×¥È¸À¸ì¤Ç¤¹¡¥Ruby¤ÏºÇ½é
¤«¤é½ã¿è¤Ê¥ª¥Ö¥¸¥§¥¯¥È»Ø¸þ¸À¸ì¤È¤·¤ÆÀß·×¤µ¤ì¤Æ¤¤¤Þ¤¹¤«¤é¡¤¥ª¥Ö¥¸¥§¥¯¥È
»Ø¸þ¥×¥í¥°¥é¥ß¥ó¥°¤ò¼ê·Ú¤Ë¹Ô¤¦»ö¤¬½ÐÍè¤Þ¤¹¡¥¤â¤Á¤í¤óÄÌ¾ï¤Î¼êÂ³¤­·¿¤Î¥×
¥í¥°¥é¥ß¥ó¥°¤â²ÄÇ½¤Ç¤¹¡¥

%description -l pl
Ruby to interpretowany jêzyk skryptowy, w sam raz dla ³atwego i
szybkiego pisania zorientowanych obiektowo programów. Ma wiele funkcji
u³atwiaj±cych przetwarzanie plików tekstowych i wykonywanie prac
zwi±zanych z zarz±dzaniem systemu (podobnie jak Perl). Jest prosty,
rozszerzalny i przeno¶ny.

Ten pakiet zawiera tylko bibliotekê dzielon± i interpreter ruby.
Zainstaluj pakiet ruby-modules, je¿eli potrzebujesz w pe³ni
funkcjonalnego ¶rodowiska ruby.

%description -l pt_BR
Ruby é uma linguagem de script interpretada de programação orientada a
objeto. Possui diversas características para processamento de texto. É
simples, extensível e direta.

%package modules
Summary:	Ruby standard modules and utilities
Summary(pl):	Standardowe modu³y i narzêdzia dla jêzyka Ruby
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

%description modules -l pl
Standardowe modu³y i narzêdzia Ruby:
- erb - ma³y eRuby
- rdoc - narzêdzie do dokumentowania kodu ¼ród³owego
- irb - interaktywny Ruby
- ri - interaktywna dokumentacja Ruby
- testrb - automatyczny runner dla Ruby Test::Unit

%package tk
Summary:	Ruby/Tk bindings
Summary(pl):	Wi±zania Ruby/Tk
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description tk
This pachage contains Ruby/Tk bindings.

%description tk -l pl
Ten pakiet zawiera wi±zania Ruby/Tk.

%package devel
Summary:	Ruby development libraries
Summary(pl):	Biblioteki programistyczne interpretera jêzyka Ruby
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description devel
Ruby development libraries.

%description devel -l pl
Biblioteki programistyczne interpretera jêzyka Ruby.

%package static
Summary:	Ruby static libraries
Summary(pl):	Biblioteki statyczne Ruby
Group:		Development/Languages
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Ruby static libraries.

%description static -l pl
Biblioteki statyczne Ruby.

%package doc
Summary:	Ruby HTML documentation
Summary(pl):	Dokumentacja HTML do Ruby
Group:		Documentation

%description doc
Ruby HTML documentation: FAQ, guide, core and standard library.

%description doc -l pl
Dokumentacja HTML do Ruby: FAQ, przewodnik, dokumentacja dla core i
stdlib.

%package doc-ri
Summary:	Ruby ri documentation
Summary(pl):	Dokumentacja Ruby w formacie ri
Group:		Documentation
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description doc-ri
Ruby ri documentation.

%description doc-ri -l pl
Dokumentacja Ruby w formacie ri.

%package examples
Summary:	Ruby examples
Summary(pl):	Przyk³ady dla jêzyka Ruby
Group:		Development/Languages

%description examples
Ruby examples.

%description examples -l pl
Przyk³ady programów w jêzyku Ruby.

%package emacs-mode
Summary:	Ruby mode and debugger for Emacs
Summary(pl):	Tryb Ruby i debugger dla Emacsa
Group:		Development/Tools
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}
Requires:	emacs-common

%description emacs-mode
Ruby mode and debugger for Emacs.

%description emacs-mode -l pl
Tryb Ruby i debugger dla Emacsa.

%prep
%setup -q -a1 -a2 -a3 -a5 -a6 -a7
%patch0 -p1
%patch1 -p1
%patch2 -p1

find . -name '*.rb' -o -name '*.cgi' -o -name '*.test' -o -name 'ruby.1' \
	-o -name 'ruby.info*' -o -name '*.html' -o -name '*.tcl' -o -name '*.texi' \
	| xargs %{__sed} -i 's,/usr/local/bin/,%{_bindir}/,'

%build
cp -f /usr/share/automake/config.sub .

cd oniguruma
%configure \
	--with-rubydir=..
%{__make} 18
cd ..

%{__autoconf}
%configure \
	--enable-shared \
	--enable-pthread \
	--with-X11-lib=/usr/X11R6/%{_lib}

%{__make}
%{__make} clean -C %{name}-texi-1.4-en
%{__make} info -C %{name}-texi-1.4-en

mkdir rdoc

RUBYLIB="lib:`find ext/ .ext/ -type d | tr '\n' ':'`"
export RUBYLIB

LD_LIBRARY_PATH=. ./ruby bin/rdoc --inline-source --op rdoc/core \
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

LD_LIBRARY_PATH=. ./ruby bin/rdoc --ri -o ri/%{ruby_ver}/system \
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

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_mandir}/man1,%{_examplesdir}/%{name}-%{version},%{ruby_ridir}}
install -d $RPM_BUILD_ROOT{%{_datadir}/%{name},%{_emacs_lispdir}/{%{name}-mode,site-start.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install %{name}-texi-1.4-en/ruby.info* $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE8} $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE9} $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE10} $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE11} $RPM_BUILD_ROOT%{_mandir}/man1

cp -Rf ruby-uguide guide
cp -Rf rubyfaq faq

cp -Rf ri/%{ruby_ver}/system/* $RPM_BUILD_ROOT%{ruby_ridir}

# ruby emacs mode - borrowed from FC-4
%if %{with emacs}
install misc/*.el $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode
rm -f $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode/rubydb2x.el
install %{SOURCE12} $RPM_BUILD_ROOT%{_emacs_lispdir}/site-start.d
cat << EOF > path.el
(setq load-path (cons "." load-path) byte-compile-warnings nil)
EOF
emacs --no-site-file -q -batch -l path.el -f batch-byte-compile $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode/*.el
rm -f path.el*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir %{_infodir} >/dev/null 2>&1
/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README README.EXT ChangeLog ToDo
%attr(755,root,root) %{_bindir}/ruby
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_mandir}/man1/ruby.1*
%{_infodir}/*.info*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{ruby_ver}
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*
%dir %{_ulibdir}/%{name}/site_ruby
%dir %{_ulibdir}/%{name}/site_ruby/%{ruby_ver}
%dir %{_ulibdir}/%{name}/site_ruby/%{ruby_ver}/*-linux*
%dir %{_datadir}/%{name}
%dir %{_datadir}/ri
%dir %{_datadir}/ri/%{ruby_ver}
%dir %{_datadir}/ri/%{ruby_ver}/system

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/%{name}/%{ruby_ver}/*/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files tk
%defattr(644,root,root,755)
%{_libdir}/%{name}/%{ruby_ver}/tcltk.rb
%{_libdir}/%{name}/%{ruby_ver}/tk*.rb
%{_libdir}/%{name}/%{ruby_ver}/tk
%{_libdir}/%{name}/%{ruby_ver}/tkextlib
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/t*.so

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erb
%attr(755,root,root) %{_bindir}/irb
%attr(755,root,root) %{_bindir}/rdoc
%attr(755,root,root) %{_bindir}/ri
%attr(755,root,root) %{_bindir}/testrb
%{_libdir}/%{name}/%{ruby_ver}/bigdecimal
%{_libdir}/%{name}/%{ruby_ver}/cgi
%{_libdir}/%{name}/%{ruby_ver}/date
%{_libdir}/%{name}/%{ruby_ver}/dl
%{_libdir}/%{name}/%{ruby_ver}/drb
%{_libdir}/%{name}/%{ruby_ver}/io
%{_libdir}/%{name}/%{ruby_ver}/irb
%{_libdir}/%{name}/%{ruby_ver}/net
%{_libdir}/%{name}/%{ruby_ver}/openssl
%{_libdir}/%{name}/%{ruby_ver}/optparse
%{_libdir}/%{name}/%{ruby_ver}/racc
%{_libdir}/%{name}/%{ruby_ver}/rdoc
%{_libdir}/%{name}/%{ruby_ver}/rexml
%{_libdir}/%{name}/%{ruby_ver}/rinda
%{_libdir}/%{name}/%{ruby_ver}/rss
%{_libdir}/%{name}/%{ruby_ver}/runit
%{_libdir}/%{name}/%{ruby_ver}/shell
%{_libdir}/%{name}/%{ruby_ver}/soap
%{_libdir}/%{name}/%{ruby_ver}/test
%{_libdir}/%{name}/%{ruby_ver}/uri
%{_libdir}/%{name}/%{ruby_ver}/webrick
%{_libdir}/%{name}/%{ruby_ver}/wsdl
%{_libdir}/%{name}/%{ruby_ver}/xmlrpc
%{_libdir}/%{name}/%{ruby_ver}/xsd
%{_libdir}/%{name}/%{ruby_ver}/yaml
%{_libdir}/%{name}/%{ruby_ver}/[A-Za-s]*.rb
%{_libdir}/%{name}/%{ruby_ver}/tempfile.rb
%{_libdir}/%{name}/%{ruby_ver}/thread.rb
%{_libdir}/%{name}/%{ruby_ver}/thwait.rb
%{_libdir}/%{name}/%{ruby_ver}/time.rb
%{_libdir}/%{name}/%{ruby_ver}/timeout.rb
%{_libdir}/%{name}/%{ruby_ver}/tmpdir.rb
%{_libdir}/%{name}/%{ruby_ver}/tracer.rb
%{_libdir}/%{name}/%{ruby_ver}/tsort.rb
%{_libdir}/%{name}/%{ruby_ver}/[u-z]*.rb
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/digest
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/io
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/racc
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/[a-s]*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/[u-z]*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/digest/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/io/*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/racc/*.so
%{_libdir}/%{name}/%{ruby_ver}/*-linux*/rbconfig.rb
%{_mandir}/man1/erb.1*
%{_mandir}/man1/irb.1*
%{_mandir}/man1/rdoc.1*
%{_mandir}/man1/ri.1*
%{_mandir}/man1/testrb.1*

%files doc
%defattr(644,root,root,755)
%doc faq guide rdoc

%files doc-ri
%defattr(644,root,root,755)
%{_datadir}/ri/%{ruby_ver}/system/*

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%if %{with emacs}
%files emacs-mode
%defattr(644,root,root,755)
%doc misc/*
%dir %{_emacs_lispdir}/%{name}-mode
%{_emacs_lispdir}/%{name}-mode/*.elc
%{_emacs_lispdir}/site-start.d/*.el
%endif
