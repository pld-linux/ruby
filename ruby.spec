%define		ruby_ridir	%{_datadir}/ri/1.8/system

Summary:	Ruby - interpreted scripting language
Summary(ja):	¥ª¥Ö¥¸¥§¥¯¥È»Ø¸þ¸À¸ìRuby¥¤¥ó¥¿¥×¥ê¥¿
Summary(pl):	Ruby - interpretowany jêzyk skryptowy
Summary(pt_BR):	Linguagem de script orientada a objeto
Summary(zh_CN):	ruby - Ò»ÖÖ¿ìËÙ¸ßÐ§µÄÃæÏò¶ÔÏó½Å±¾±à³ÌÓïÑÔ
Name:		ruby
Version:	1.8.2
Release:	3
Epoch:		1
License:	The Ruby License
Group:		Development/Languages
#Source0:	ftp://ftp.ruby-lang.org/pub/ruby/stable-snapshot.tar.gz
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/%{name}-%{version}.tar.gz
# Source0-md5:	8ffc79d96f336b80f2690a17601dea9b
Source1:	http://www.ibiblio.org/pub/languages/ruby/doc/%{name}-texi-1.4-en.tar.gz
# Source1-md5:	839fda4af52b5c5c6d21f879f7fc62bf
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/%{name}-uguide-981227.tar.gz
# Source2-md5:	24eadcd067278901da9ad70efb146b07
Source3:	http://www.ibiblio.org/pub/languages/ruby/doc/%{name}faq-990927.tar.gz
# Source3-md5:	634c25b14e19925d10af3720d72e8741
Source4:	irb.1
Source5:	http://www.geocities.jp/kosako3/oniguruma/archive/onigd2_4_0.tar.gz
# Source5-md5:	f64bad67181b02fbd67fac16710537f3
%define stdlibdoc_version	0.9.13
Source6:	http://www.ruby-doc.org/downloads/stdlib/ruby-doc-stdlib-%{stdlibdoc_version}.tgz
# Source6-md5:	39dab8db652dad23ad8951f851549f06
Source7:	http://www.ruby-doc.org/downloads/Ruby-1.8.1_ri_data.zip
# Source7-md5:	96e97cdfa55ed197e0e6c39159394c82
Patch0:		%{name}-info.patch
Patch1:		%{name}-LIB_PREFIX.patch
Patch2:		%{name}-ia64.patch
Patch3:		%{name}-mkmf-shared.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	texinfo
BuildRequires:	tk-devel
BuildRequires:	unzip
Requires(post,postun): /sbin/ldconfig
Obsoletes:	ruby-doc
Obsoletes:	rdoc
Obsoletes:	ruby-REXML
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_ulibdir	%{_prefix}/lib

# bleh, some nasty (gcc or ruby) bug still not fixed
# (SEGV or "unexpected break" on miniruby run during build)
%define		specflags_ia64	-O0

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text
files and to do system management tasks (as in Perl). It is simple,
straight-forward, extensible, and portable.

%description -l ja
Ruby¤Ï¥·¥ó¥×¥ë¤«¤Ä¶¯ÎÏ¤Ê¥ª¥Ö¥¸¥§¥¯¥È»Ø¸þ¥¹¥¯¥ê¥×¥È¸À¸ì¤Ç¤¹¡¥Ruby¤ÏºÇ½é
¤«¤é½ã¿è¤Ê¥ª¥Ö¥¸¥§¥¯¥È»Ø¸þ¸À¸ì¤È¤·¤ÆÀß·×¤µ¤ì¤Æ¤¤¤Þ¤¹¤«¤é¡¤¥ª¥Ö¥¸¥§¥¯¥È
»Ø¸þ¥×¥í¥°¥é¥ß¥ó¥°¤ò¼ê·Ú¤Ë¹Ô¤¦»ö¤¬½ÐÍè¤Þ¤¹¡¥¤â¤Á¤í¤óÄÌ¾ï¤Î¼êÂ³¤­·¿¤Î¥×
¥í¥°¥é¥ß¥ó¥°¤â²ÄÇ½¤Ç¤¹¡¥

Ruby¤Ï¥Æ¥­¥¹¥È½èÍý´Ø·¸¤ÎÇ½ÎÏ¤Ê¤É¤ËÍ¥¤ì¡¤Perl¤ÈÆ±¤¸¤¯¤é¤¤¶¯ÎÏ¤Ç¤¹¡¥¤µ¤é
¤Ë¥·¥ó¥×¥ë¤ÊÊ¸Ë¡¤È¡¤Îã³°½èÍý¤ä¥¤¥Æ¥ì¡¼¥¿¤Ê¤É¤Îµ¡¹½¤Ë¤è¤Ã¤Æ¡¤¤è¤êÊ¬¤«¤ê
¤ä¤¹¤¤¥×¥í¥°¥é¥ß¥ó¥°¤¬½ÐÍè¤Þ¤¹¡¥

%description -l pl
Ruby to interpretowany jêzyk skryptowy, w sam raz dla ³atwego i
szybkiego pisania zorientowanych obiektowo programów. Ma wiele funkcji
u³atwiaj±cych przetwarzanie plików tekstowych i wykonywanie prac
zwi±zanych z zarz±dzaniem systemu (podobnie jak Perl). Jest prosty,
rozszerzalny i przeno¶ny.

%description -l pt_BR
Ruby é uma linguagem de script interpretada de programação
orientada a objeto. Possui diversas características para
processamento de texto. É simples, extensível e direta.

%package tk
Summary:	Ruby/Tk bindings
Summary(pl):	Wi±zania Ruby/Tk
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description tk
This pachage contains Ruby/Tk bindings.

%description tk -l pl
Ten pakiet zawiera wi±zania Ruby/Tk.

%package devel
Summary:	Ruby development libraries
Summary(pl):	Biblioteki programistyczne interpretera jêzyka Ruby
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Ruby development libraries.

%description devel -l pl
Biblioteki programistyczne interpretera jêzyka Ruby.

%package static
Summary:	Ruby static libraries
Summary(pl):	Biblioteki statyczne Ruby
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description static
Ruby static libraries.

%description devel -l pl
Biblioteki statyczne Ruby.

%prep
%setup -q -a1 -a2 -a3 -a5 -a6 -a7 
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

find . -name '*.rb' -or -name '*.cgi' -or -name '*.test' | xargs perl -pi -e "s#/usr/local/bin#bin#"

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
	--with-X11-lib=/usr/X11R6/%{_lib} \
	--with-sitedir=%{_libdir}/ruby/site_ruby
%{__make}

%{__make} info -C %{name}-texi-1.4-en

mkdir rdoc

RUBYLIB=lib:`ls ext/*/ | xargs | sed -e 's! !:!g'`
export RUBYLIB

LD_LIBRARY_PATH=. ./ruby bin/rdoc -o rdoc/core array.c bignum.c class.c compar.c dir.c dln.c dmyext.c enum.c \
	error.c eval.c file.c gc.c hash.c inits.c io.c lex.c main.c marshal.c \
	math.c numeric.c object.c pack.c parse.c prec.c process.c random.c range.c \
	re.c regex.c ruby.c signal.c sprintf.c st.c string.c struct.c time.c util.c \
	variable.c version.c \
	lib/English.rb lib/abbrev.rb lib/base64.rb lib/benchmark.rb lib/cgi.rb \
	lib/cgi/session.rb lib/complex.rb lib/date.rb lib/fileutils.rb lib/find.rb \
	lib/generator.rb lib/logger.rb lib/matrix.rb lib/observer.rb lib/pathname.rb \
	lib/set.rb lib/shellwords.rb lib/singleton.rb lib/tempfile.rb \
	lib/test/unit.rb lib/thread.rb lib/thwait.rb lib/time.rb lib/yaml.rb

mv ruby-doc-stdlib-%{stdlibdoc_version}/stdlib rdoc/stdlib

mv ri/1.8/site ri/1.8/system

LD_LIBRARY_PATH=. ./ruby bin/rdoc --ri -o ri/1.8/system array.c bignum.c class.c compar.c dir.c dln.c \
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

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install %{name}-texi-1.4-en/ruby.info* $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1

mv -f ruby-uguide guide
mv -f rubyfaq faq

cp -a ri/1.8/system/* $RPM_BUILD_ROOT%{ruby_ridir}

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
%doc guide faq misc README README.EXT ChangeLog ToDo
%doc rdoc
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/1.8
%{_libdir}/%{name}/1.8/bigdecimal
%{_libdir}/%{name}/1.8/cgi
%{_libdir}/%{name}/1.8/date
%{_libdir}/%{name}/1.8/dl
%{_libdir}/%{name}/1.8/drb
%{_libdir}/%{name}/1.8/io
%{_libdir}/%{name}/1.8/irb
%{_libdir}/%{name}/1.8/net
%{_libdir}/%{name}/1.8/openssl
%{_libdir}/%{name}/1.8/optparse
%{_libdir}/%{name}/1.8/racc
%{_libdir}/%{name}/1.8/rdoc
%{_libdir}/%{name}/1.8/rexml
%{_libdir}/%{name}/1.8/rinda
%{_libdir}/%{name}/1.8/rss
%{_libdir}/%{name}/1.8/runit
%{_libdir}/%{name}/1.8/shell
%{_libdir}/%{name}/1.8/soap
%{_libdir}/%{name}/1.8/test
%{_libdir}/%{name}/1.8/uri
%{_libdir}/%{name}/1.8/webrick
%{_libdir}/%{name}/1.8/wsdl
%{_libdir}/%{name}/1.8/xmlrpc
%{_libdir}/%{name}/1.8/xsd
%{_libdir}/%{name}/1.8/yaml
%{_libdir}/%{name}/1.8/[A-Za-s]*.rb
%{_libdir}/%{name}/1.8/tempfile.rb
%{_libdir}/%{name}/1.8/thread.rb
%{_libdir}/%{name}/1.8/thwait.rb
%{_libdir}/%{name}/1.8/time.rb
%{_libdir}/%{name}/1.8/timeout.rb
%{_libdir}/%{name}/1.8/tmpdir.rb
%{_libdir}/%{name}/1.8/tracer.rb
%{_libdir}/%{name}/1.8/tsort.rb
%{_libdir}/%{name}/1.8/[u-z]*.rb
%dir %{_libdir}/%{name}/1.8/*-linux*
%dir %{_libdir}/%{name}/1.8/*-linux*/digest
%dir %{_libdir}/%{name}/1.8/*-linux*/io
%dir %{_libdir}/%{name}/1.8/*-linux*/racc
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/[a-s]*.so
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/[u-z]*.so
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/digest/*.so
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/io/*.so
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/racc/*.so
%{_libdir}/%{name}/1.8/*-linux*/rbconfig.rb
%dir %{_ulibdir}/%{name}/site_ruby
%dir %{_ulibdir}/%{name}/site_ruby/1.8
%dir %{_ulibdir}/%{name}/site_ruby/1.8/*-linux*
%{_datadir}/ri
%{_mandir}/*/*
%{_infodir}/*.info*
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/%{name}/1.8/*/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a

%files tk
%defattr(644,root,root,755)
%{_libdir}/%{name}/1.8/tcltk.rb
%{_libdir}/%{name}/1.8/tk*.rb
%{_libdir}/%{name}/1.8/tk
%{_libdir}/%{name}/1.8/tkextlib
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/t*.so
