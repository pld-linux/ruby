#
# Conditional build:
%bcond_without	doc		# skip (time-consuming) docs generating; intended for speed up test builds
%bcond_without	emacs		# skip building package with ruby-mode for emacs
%bcond_without	tk		# skip building package with Tk bindings
%bcond_without	batteries	# Don't include rubygems, json or rake
%bcond_with	bootstrap	# build bootstrap version
#
%define		ruby_ver	1.9
%define		stdlibdoc_version	0.10.1
%define		patchlevel 290
%define		basever 1.9.2
%define		rake_ver	0.8.7
%define		minitest_ver	1.6.0
%define		rdoc_ver	2.5.8
Summary:	Ruby - interpreted scripting language
Summary(ja.UTF-8):	オブジェクト指向言語Rubyインタプリタ
Summary(pl.UTF-8):	Ruby - interpretowany język skryptowy
Summary(pt_BR.UTF-8):	Linguagem de script orientada a objeto
Summary(zh_CN.UTF-8):	ruby - 一种快速高效的面向对象脚本编程语言
Name:		ruby
Version:	%{basever}.%{patchlevel}
Release:	8
Epoch:		1
License:	The Ruby License
Group:		Development/Languages
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/%{name}-%{basever}-p%{patchlevel}.tar.bz2
# Source0-md5:	096758c3e853b839dc980b183227b182
Source1:	http://www.ruby-doc.org/download/%{name}-doc-bundle.tar.gz
# Source1-md5:	ad1af0043be98ba1a4f6d0185df63876
Source2:	http://www.ruby-doc.org/download/stdlib/%{name}-doc-stdlib-%{stdlibdoc_version}.tgz
# Source2-md5:	5437c281b44e7a4af142d2bd35eba407
Source100:	ftp://ftp.ruby-lang.org/pub/ruby/1.8/%{name}-1.8.7-p330.tar.gz
# Source100-md5:	50a49edb787211598d08e756e733e42e
Source3:	rdoc.1
Source4:	testrb.1
Source5:	%{name}-mode-init.el
Patch0:		%{name}-mkmf-shared.patch
Patch1:		%{name}-lib64.patch
Patch2:		%{name}-ffs.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
%{?with_emacs:BuildRequires:	emacs}
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	readline-devel >= 4.2
%{!?with_bootstrap:BuildRequires:	ruby-modules}
BuildRequires:	sed >= 4.0
BuildRequires:	yaml-devel
%if %{with tk}
BuildRequires:	tk-devel
%endif
Requires(post,postun):	/sbin/ldconfig
Provides:	ruby(ver) = %{ruby_ver}
Obsoletes:	rdoc
Obsoletes:	ruby-REXML
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread
%if %{with batteries}
Provides:	ruby-rake = %{rake_ver}
# which versions?
Provides:	ruby-json
Provides:	ruby-rubygems
Obsoletes:	ruby-json
Obsoletes:	ruby-rake
Obsoletes:	ruby-rubygems
%endif
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
指向プログラミングを手軽に行う事が出来ます．もちろん通常の手続き型のプ ログラミングも可能です．

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
Obsoletes:	ruby-minitest

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
%setup -q -n %{name}-%{basever}-p%{patchlevel} -a1 -a2 -a100
%patch0 -p1
%patch1 -p1
%patch2 -p1

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

find -type f '(' -name '*.rb' -o -name '*.cgi' -o -name '*.test' \
	-o -name 'ruby.1' -o -name '*.html' -o -name '*.tcl' ')' \
	| xargs %{__sed} -i 's,/usr/local/bin/,%{_bindir}/,'

%build
cp -f /usr/share/automake/config.sub .

# build ruby-1.8.7 first
%if %{with bootstrap}
cd %{name}-1.8.7-p330
%configure
%{__make}
cd ..
%endif

%{__autoconf}
%configure \
	%{?with_bootstrap:--with-baseruby=%{name}-1.8.7-p330/miniruby} \
	--enable-shared \
	--enable-pthread \
	--with-ruby-version=minor

%{__make} -j1 %{?with_bootstrap:BASERUBY="ruby-1.8.7-p330/miniruby -I./ruby-1.8.7-p330/lib"}

%if %{with doc}
%{__make} -j1 rdoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir},%{_examplesdir}/%{name}-%{version}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man1
cp -a %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1

%if %{without batteries}
# packaged separately
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/%{ruby_ver}/{rubygems,rake,json}
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/%{name}/%{ruby_ver}/*-linux*/json
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/%{ruby_ver}/{rake,rubygems,json}.rb
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{gem,rake}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/rake*
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ri/%{ruby_ver}/system/JSON
%endif

# ruby emacs mode - borrowed from FC-4
%if %{with emacs}
install -d $RPM_BUILD_ROOT%{_emacs_lispdir}/{%{name}-mode,site-start.d}
cp -a misc/*.el $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode
%{__rm} $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode/rubydb2x.el*
install -p %{SOURCE5} $RPM_BUILD_ROOT%{_emacs_lispdir}/site-start.d
cat << 'EOF' > path.el
(setq load-path (cons "." load-path) byte-compile-warnings nil)
EOF
emacs --no-site-file -q -batch -l path.el -f batch-byte-compile $RPM_BUILD_ROOT%{_emacs_lispdir}/%{name}-mode/*.el
%{__rm} path.el*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS LEGAL README README.EXT ChangeLog ToDo
%attr(755,root,root) %{_bindir}/ruby
%if %{with batteries}
%attr(755,root,root) %{_bindir}/gem
%attr(755,root,root) %{_bindir}/rake
%endif
%attr(755,root,root) %{_libdir}/libruby.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libruby.so.1.9
%{_mandir}/man1/ruby.1*
%if %{with batteries}
%{_mandir}/man1/rake.1*
%endif
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/%{ruby_ver}
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*
%dir %{_libdir}/%{name}/site_ruby
%dir %{_libdir}/%{name}/site_ruby/%{ruby_ver}
%dir %{_libdir}/%{name}/site_ruby/%{ruby_ver}/*-linux*
%dir %{_libdir}/%{name}/vendor_ruby
%dir %{_libdir}/%{name}/vendor_ruby/%{ruby_ver}
%dir %{_libdir}/%{name}/vendor_ruby/%{ruby_ver}/*-linux*
%dir %{_datadir}/ri
%dir %{_datadir}/ri/%{ruby_ver}
%dir %{_datadir}/ri/%{ruby_ver}/system
%dir %{ruby_rdocdir}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libruby.so
%{_includedir}/%{name}-%{ruby_ver}

%files static
%defattr(644,root,root,755)
%{_libdir}/libruby-static.a

%if %{with tk}
%files tk
%defattr(644,root,root,755)
%{_libdir}/%{name}/%{ruby_ver}/tcltk.rb
%{_libdir}/%{name}/%{ruby_ver}/tk*.rb
%{_libdir}/%{name}/%{ruby_ver}/tk
%{_libdir}/%{name}/%{ruby_ver}/tkextlib
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/t*.so
%endif

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
%{_libdir}/%{name}/%{ruby_ver}/digest
%{_libdir}/%{name}/%{ruby_ver}/dl
%{_libdir}/%{name}/%{ruby_ver}/drb
%{_libdir}/%{name}/%{ruby_ver}/fiddle
%{_libdir}/%{name}/%{ruby_ver}/irb
%{_libdir}/%{name}/%{ruby_ver}/minitest
%{_libdir}/%{name}/%{ruby_ver}/net
%{_libdir}/%{name}/%{ruby_ver}/openssl
%{_libdir}/%{name}/%{ruby_ver}/optparse
%if %{with batteries}
%{_libdir}/%{name}/%{ruby_ver}/json
%{_libdir}/%{name}/%{ruby_ver}/rake
%{_libdir}/%{name}/%{ruby_ver}/rubygems
%endif
%{_libdir}/%{name}/%{ruby_ver}/psych
%{_libdir}/%{name}/%{ruby_ver}/racc
%{_libdir}/%{name}/%{ruby_ver}/rbconfig
%{_libdir}/%{name}/%{ruby_ver}/rdoc
%{_libdir}/%{name}/%{ruby_ver}/rexml
%{_libdir}/%{name}/%{ruby_ver}/rinda
%{_libdir}/%{name}/%{ruby_ver}/ripper
%{_libdir}/%{name}/%{ruby_ver}/rss
%{_libdir}/%{name}/%{ruby_ver}/shell
%{_libdir}/%{name}/%{ruby_ver}/syck
%{_libdir}/%{name}/%{ruby_ver}/test
%{_libdir}/%{name}/%{ruby_ver}/uri
%{_libdir}/%{name}/%{ruby_ver}/webrick
%{_libdir}/%{name}/%{ruby_ver}/xmlrpc
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
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/[a-s]*.so
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/[u-z]*.so
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/digest
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/digest/*.so
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/dl
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/dl/callback.so
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc/*.so
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc/trans
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/enc/trans/*.so
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/io
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/io/*.so
%if %{with batteries}
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/json
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/json/ext
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/json/ext/*.so
%endif
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/mathn
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/mathn/*.so
%dir %{_libdir}/%{name}/%{ruby_ver}/*-linux*/racc
%attr(755,root,root) %{_libdir}/%{name}/%{ruby_ver}/*-linux*/racc/*.so
%{_libdir}/%{name}/%{ruby_ver}/*-linux*/rbconfig.rb
%dir %{_libdir}/%{name}/gems
%dir %{_libdir}/%{name}/gems/%{ruby_ver}
%dir %{_libdir}/%{name}/gems/%{ruby_ver}/specifications
%if %{with batteries}
%{_libdir}/%{name}/gems/%{ruby_ver}/specifications/minitest-%{minitest_ver}.gemspec
%{_libdir}/%{name}/gems/%{ruby_ver}/specifications/rake-%{rake_ver}.gemspec
%{_libdir}/%{name}/gems/%{ruby_ver}/specifications/rdoc-%{rdoc_ver}.gemspec
%endif
%{_mandir}/man1/erb.1*
%{_mandir}/man1/irb.1*
%{_mandir}/man1/rdoc.1*
%{_mandir}/man1/ri.1*
%{_mandir}/man1/testrb.1*

%files doc
%defattr(644,root,root,755)
%doc ruby-doc-bundle/*
%{?with_doc:%doc ruby-doc-stdlib-%{stdlibdoc_version}/stdlib}

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
%dir %{_emacs_lispdir}/%{name}-mode
%{_emacs_lispdir}/%{name}-mode/*.elc
%{_emacs_lispdir}/site-start.d/*.el
%endif
