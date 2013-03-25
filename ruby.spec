#
# TODO:
#	- include ext/ in docs
#	- replace ri with fastri
#	- patch ri to search multiple indexes (one per package), so RPMs can install ri docs
#
# Conditional build:
%bcond_without	doc		# skip (time-consuming) docs generating; intended for speed up test builds
%bcond_without	tk		# skip building package with Tk bindings
%bcond_without	batteries	# Don't include rubygems, json or rake
%bcond_without	verpath	# LOAD_PATH with version number
%bcond_with	bootstrap	# build bootstrap version

%define		ruby_version	1.9
%define		basever		1.9.3
%define		patchlevel	392
%define		doc_version	1_9_3
%define		json_ver	1.5.5
%define		rake_ver	0.9.2.2
%define		rubygems_ver	1.8.11
%define		minitest_ver	2.5.1
%define		rdoc_ver	3.9.5
Summary:	Ruby - interpreted scripting language
Summary(ja.UTF-8):	オブジェクト指向言語Rubyインタプリタ
Summary(pl.UTF-8):	Ruby - interpretowany język skryptowy
Summary(pt_BR.UTF-8):	Linguagem de script orientada a objeto
Summary(zh_CN.UTF-8):	ruby - 一种快速高效的面向对象脚本编程语言
Name:		ruby
Version:	%{basever}.%{patchlevel}
Release:	0.11
Epoch:		1
License:	The Ruby License
Group:		Development/Languages
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/%{ruby_version}/%{name}-%{basever}-p%{patchlevel}.tar.bz2
# Source0-md5:	a810d64e2255179d2f334eb61fb8519c
Source1:	http://www.ruby-doc.org/download/%{name}-doc-bundle.tar.gz
# Source1-md5:	ad1af0043be98ba1a4f6d0185df63876
Source2:	http://www.ruby-doc.org/downloads/%{name}_%{doc_version}_stdlib_rdocs.tgz
# Source2-md5:	ec622612428672c432b6f65dd31a84b5
Source3:	http://www.ruby-doc.org/downloads/%{name}_%{doc_version}_core_rdocs.tgz
# Source3-md5:	1892aadde51d36106c513bced2193dff
Source100:	ftp://ftp.ruby-lang.org/pub/ruby/1.8/%{name}-1.8.7-p330.tar.gz
# Source100-md5:	50a49edb787211598d08e756e733e42e
Source4:	rdoc.1
Source5:	testrb.1
Source6:	%{name}-mode-init.el
Patch0:		%{name}-lib64.patch
Patch1:		%{name}-ffs.patch
Patch2:		fix-bison-invocation.patch
# http://redmine.ruby-lang.org/issues/5231
Patch3:		disable-versioned-paths.patch
# TODO: Should be submitted upstream?
Patch4:		arch-specific-dir.patch
# http://redmine.ruby-lang.org/issues/5281
Patch5:		site-and-vendor-arch-flags.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	db-devel
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
%{!?with_bootstrap:BuildRequires:	ruby-modules}
BuildRequires:	sed >= 4.0
BuildRequires:	yaml-devel
%if %{with tk}
BuildRequires:	tk-devel
%endif
Requires(post,postun):	/sbin/ldconfig
Provides:	ruby(ver) = %{ruby_version}
Obsoletes:	rdoc
Obsoletes:	ruby-REXML
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread
%if %{with batteries}
Provides:	json = %{json_ver}
Provides:	rake = %{rake_ver}
Provides:	ruby-json = %{json_ver}
Provides:	ruby-rake = %{rake_ver}
Provides:	ruby-rubygems = %{rubygems_ver}
Provides:	rubygems = %{rubygems_ver}
Obsoletes:	ruby-json
Obsoletes:	ruby-rake
Obsoletes:	ruby-rubygems
%endif
Conflicts:	ruby-activesupport < 2.3.11-2
Conflicts:	ruby-activesupport2 < 2.3.11-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	gem_dir			%{_datadir}/%{name}/gems/%{ruby_version}

# The RubyGems library has to stay out of Ruby directory three, since the
# RubyGems should be share by all Ruby implementations.
%define	rubygems_dir		%{_datadir}/rubygems

%define	ruby_archdir		%{_libdir}/%{name}
%define	ruby_libdir		%{_datadir}/%{name}

# This is the local lib/arch and should not be used for packaging.
%define	sitedir			site_ruby
%define	ruby_sitedir		%{_prefix}/local/share/%{name}/%{sitedir}
%define	ruby_sitelibdir		%{_prefix}/local/share/%{name}/%{sitedir}/%{ruby_version}
%define	ruby_sitearchdir	%{_prefix}/local/%{_lib}/%{name}/%{sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the PLD repositories.
%define	vendordir		vendor_ruby
%define	ruby_vendordir		%{_datadir}/%{name}/%{vendordir}
%define	ruby_vendorarchdir	%{_libdir}/%{name}/%{vendordir}
%define	ruby_vendorlibdir	%{_datadir}/%{name}/%{vendordir}/%{ruby_version}

# TODO: drop legacy loadpaths after all ruby modules rebuilt in Th
%define	legacy_libdir		%{_libdir}/%{name}/%{ruby_version}
%define	legacy_archdir		%{_libdir}/%{name}/%{ruby_version}/%{_arch}-linux
%define	legacy_sitedir		%{_libdir}/%{name}/%{sitedir}
%define	legacy_sitelibdir	%{_libdir}/%{name}/%{sitedir}/%{ruby_version}
%define	legacy_sitearchdir	%{_libdir}/%{name}/%{sitedir}/%{ruby_version}/%{_arch}-linux
%define	legacy_vendordir	%{_libdir}/%{name}/%{vendordir}
%define	legacy_vendorlibdir	%{_libdir}/%{name}/%{vendordir}/%{ruby_version}
%define	legacy_vendorarchdir%{_libdir}/%{name}/%{vendordir}/%{ruby_version}/%{_arch}-linux

%define	legacy_siteloadpath	%{legacy_sitelibdir}\\0%{legacy_sitearchdir}\\0%{legacy_sitedir}
%define	legacy_vendorloadpath	%{legacy_vendorlibdir}\\0%{legacy_vendorarchdir}
%define	legacy_loadpath		%{legacy_archdir}
%define	legacy_loadpaths	%{legacy_siteloadpath}\\0%{legacy_vendorloadpath}\\0%{legacy_loadpath}

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
# workaround for autodep generator net getting version properly
Provides:	ruby(abi) = %{ruby_version}
Provides:	ruby-modules(ver) = %{ruby_version}
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

%prep
%if %{with bootstrap}
%setup -q -n %{name}-%{basever}-p%{patchlevel} -a1 -a2 -a3 -a100
%else
%setup -q -n %{name}-%{basever}-p%{patchlevel} -a1 -a2 -a3
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# must be regenerated with new bison
%{__rm} parse.{c,h}

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
	--with-rubylibprefix=%{ruby_libdir} \
	--with-archdir=%{ruby_archdir}/%{ruby_version} \
	--with-sitedir=%{ruby_sitelibdir} \
	--with-sitearchdir=%{ruby_sitearchdir} \
	--with-vendordir=%{ruby_vendorlibdir} \
	--with-vendorarchdir=%{ruby_vendorarchdir} \
	--with-rubygemsdir=%{rubygems_dir} \
	--with-search-path="%{legacy_loadpaths}" \
	--enable-shared \
	--enable-pthread \
	--disable-install-doc \
	%{!?with_verpath:--disable-versioned-paths} \
	--with-ruby-version=minor

%{__make} -j1 main \
	COPY="cp -p" Q= \
	%{?with_bootstrap:BASERUBY="ruby-1.8.7-p330/miniruby -I./ruby-1.8.7-p330/lib"}

%if %{with doc}
%{__make} -j1 docs
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir},%{_examplesdir}/%{name}-%{version}} \
	$RPM_BUILD_ROOT%{ruby_libdir}/%{ruby_version}/tasks \
	$RPM_BUILD_ROOT%{ruby_vendorarchdir}/%{ruby_version} \
	$RPM_BUILD_ROOT{%{legacy_archdir},%{legacy_sitelibdir},%{legacy_sitearchdir},%{legacy_vendorarchdir}} \

%{__make} install %{?with_doc:install-doc} \
	DESTDIR=$RPM_BUILD_ROOT

cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/html

%if %{without batteries}
# packaged separately
%{__rm} -r $RPM_BUILD_ROOT%{ruby_libdir}/%{ruby_version}/{rubygems,rake,json,tasks}
%{__rm} -r $RPM_BUILD_ROOT%{ruby_archdir}/%{ruby_version}/json
%{__rm} $RPM_BUILD_ROOT%{ruby_libdir}/%{ruby_version}/{rake,rubygems,json}.rb
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{gem,rake}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/rake*
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ri/%{ruby_version}/system/JSON
%endif

# too much .ri
rm -rf $RPM_BUILD_ROOT%{_datadir}/ri

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

%dir %{ruby_libdir}
%dir %{ruby_libdir}/%{ruby_version}
%dir %{ruby_archdir}
%dir %{ruby_archdir}/%{ruby_version}
%dir %{ruby_vendordir}
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorlibdir}/%{ruby_version}
%dir %{ruby_vendorarchdir}
%dir %{ruby_vendorarchdir}/%{ruby_version}

#%dir %{_datadir}/ri
#%dir %{_datadir}/ri/%{ruby_version}
#%dir %{_datadir}/ri/%{ruby_version}/system
%dir %{ruby_rdocdir}

# legacy dirs. when everything rebuilt in Th not using these dirs. drop them
%dir %{legacy_archdir}
%dir %{legacy_sitedir}
%dir %{legacy_sitelibdir}
%dir %{legacy_sitearchdir}
%dir %{legacy_vendorarchdir}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libruby.so
%{_includedir}/%{name}-%{ruby_version}
%{_pkgconfigdir}/ruby-%{ruby_version}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libruby-static.a

%if %{with tk}
%files tk
%defattr(644,root,root,755)
%{ruby_libdir}/%{ruby_version}/tcltk.rb
%{ruby_libdir}/%{ruby_version}/tk*.rb
%{ruby_libdir}/%{ruby_version}/tk
%{ruby_libdir}/%{ruby_version}/tkextlib
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/t*.so
%endif

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erb
%attr(755,root,root) %{_bindir}/irb
%attr(755,root,root) %{_bindir}/rdoc
%attr(755,root,root) %{_bindir}/ri
%attr(755,root,root) %{_bindir}/testrb
%{ruby_libdir}/%{ruby_version}/bigdecimal
%{ruby_libdir}/%{ruby_version}/cgi
%{ruby_libdir}/%{ruby_version}/date
%{ruby_libdir}/%{ruby_version}/digest
%{ruby_libdir}/%{ruby_version}/dl
%{ruby_libdir}/%{ruby_version}/drb
%{ruby_libdir}/%{ruby_version}/fiddle
%{ruby_libdir}/%{ruby_version}/io
%{ruby_libdir}/%{ruby_version}/irb
%{ruby_libdir}/%{ruby_version}/matrix
%{ruby_libdir}/%{ruby_version}/minitest
%{ruby_libdir}/%{ruby_version}/net
%{ruby_libdir}/%{ruby_version}/openssl
%{ruby_libdir}/%{ruby_version}/optparse
%if %{with batteries}
%{ruby_libdir}/%{ruby_version}/json
%{ruby_libdir}/%{ruby_version}/rake
%{ruby_libdir}/%{ruby_version}/rubygems
%dir %{ruby_libdir}/%{ruby_version}/tasks
%endif
%{ruby_libdir}/%{ruby_version}/psych
%{ruby_libdir}/%{ruby_version}/racc
%{ruby_libdir}/%{ruby_version}/rbconfig
%{ruby_libdir}/%{ruby_version}/rdoc
%{ruby_libdir}/%{ruby_version}/rexml
%{ruby_libdir}/%{ruby_version}/rinda
%{ruby_libdir}/%{ruby_version}/ripper
%{ruby_libdir}/%{ruby_version}/rss
%{ruby_libdir}/%{ruby_version}/shell
%{ruby_libdir}/%{ruby_version}/syck
%{ruby_libdir}/%{ruby_version}/test
%{ruby_libdir}/%{ruby_version}/uri
%{ruby_libdir}/%{ruby_version}/webrick
%{ruby_libdir}/%{ruby_version}/xmlrpc
%{ruby_libdir}/%{ruby_version}/yaml
%{ruby_libdir}/%{ruby_version}/[A-Za-s]*.rb
%{ruby_libdir}/%{ruby_version}/tempfile.rb
%{ruby_libdir}/%{ruby_version}/thread.rb
%{ruby_libdir}/%{ruby_version}/thwait.rb
%{ruby_libdir}/%{ruby_version}/time.rb
%{ruby_libdir}/%{ruby_version}/timeout.rb
%{ruby_libdir}/%{ruby_version}/tmpdir.rb
%{ruby_libdir}/%{ruby_version}/tracer.rb
%{ruby_libdir}/%{ruby_version}/tsort.rb
%{ruby_libdir}/%{ruby_version}/[u-z]*.rb
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/[a-s]*.so
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/[u-z]*.so
%dir %{ruby_archdir}/%{ruby_version}/digest
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/digest/*.so
%dir %{ruby_archdir}/%{ruby_version}/dl
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/dl/callback.so
%dir %{ruby_archdir}/%{ruby_version}/enc
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/enc/*.so
%dir %{ruby_archdir}/%{ruby_version}/enc/trans
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/enc/trans/*.so
%dir %{ruby_archdir}/%{ruby_version}/io
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/io/*.so
%if %{with batteries}
%dir %{ruby_archdir}/%{ruby_version}/json
%dir %{ruby_archdir}/%{ruby_version}/json/ext
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/json/ext/*.so
%endif
%dir %{ruby_archdir}/%{ruby_version}/mathn
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/mathn/*.so
%dir %{ruby_archdir}/%{ruby_version}/racc
%attr(755,root,root) %{ruby_archdir}/%{ruby_version}/racc/*.so
%{ruby_archdir}/%{ruby_version}/rbconfig.rb

# parents of gem_dir
%dir %{_datadir}/%{name}/gems
#%dir %{_datadir}/%{name}/gems/%{ruby_version}
%dir %{_datadir}/%{name}/gems/%{ruby_version}/gems

%dir %{gem_dir}
%dir %{gem_dir}/specifications
%{gem_dir}/specifications/io-console-*.gemspec
%{gem_dir}/specifications/bigdecimal-*.gemspec
%if %{with batteries}
%dir %{gem_dir}/gems/rake-%{rake_ver}
%dir %{gem_dir}/gems/rake-%{rake_ver}/bin
%attr(755,root,root) %{gem_dir}/gems/rake-%{rake_ver}/bin/rake
%dir %{gem_dir}/gems/rdoc-%{rdoc_ver}
%dir %{gem_dir}/gems/rdoc-%{rdoc_ver}/bin
%attr(755,root,root) %{gem_dir}/gems/rdoc-%{rdoc_ver}/bin/rdoc
%attr(755,root,root) %{gem_dir}/gems/rdoc-%{rdoc_ver}/bin/ri
%{gem_dir}/specifications/minitest-%{minitest_ver}.gemspec
%{gem_dir}/specifications/rake-%{rake_ver}.gemspec
%{gem_dir}/specifications/rdoc-%{rdoc_ver}.gemspec
%{gem_dir}/specifications/json-%{json_ver}.gemspec
%endif
%{_mandir}/man1/erb.1*
%{_mandir}/man1/irb.1*
%{_mandir}/man1/rdoc.1*
%{_mandir}/man1/ri.1*
%{_mandir}/man1/testrb.1*

%files doc
%defattr(644,root,root,755)
%doc ruby-doc-bundle/*
%{?with_doc:%doc ruby_%{doc_version}_stdlib}
%{?with_doc:%doc ruby_%{doc_version}_core}

%if %{with doc}
%files doc-ri
%defattr(644,root,root,755)
%{_datadir}/ri/%{ruby_version}/system/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
