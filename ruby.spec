# TODO:
#	- include ext/ in docs
#	- replace ri with fastri
#	- patch ri to search multiple indexes (one per package), so RPMs can install ri docs
#   - fix inconsistencies with versioned vs not-versioned dirs (see dirname hacks in configure)
#
# Conditional build:
%bcond_without	doc		# skip (time-consuming) docs generating; intended for speed up test builds
%bcond_without	tk		# skip building package with Tk bindings
%bcond_without	batteries	# Don't include rubygems, json, rake, minitest
%bcond_without	default_ruby	# use this Ruby as default system Ruby
%bcond_with	bootstrap	# build bootstrap version

%define		rel		0.2
%define		ruby_version	2.0
%define		ver_suffix	20
%define		basever		2.0.0
%define		patchlevel	353

%define		ruby_suffix %{!?with_default_ruby:%{ver_suffix}}
%define		doc_version	1_9_3

%define		bigdecimal_ver	1.2.0
%define		io_console_ver	0.4.2
%define		irb_ver		0.9.6
%define		json_ver	1.7.7
%define		minitest_ver	4.3.2
%define		psych_ver	2.0.0
%define		rake_ver	0.9.6
%define		rdoc_ver	4.0.0
%define		rubygems_ver	2.0.14
%define		test_unit_ver	2.0.0.0

%define		oname	ruby
Summary:	Ruby - interpreted scripting language
Summary(ja.UTF-8):	オブジェクト指向言語Rubyインタプリタ
Summary(pl.UTF-8):	Ruby - interpretowany język skryptowy
Summary(pt_BR.UTF-8):	Linguagem de script orientada a objeto
Summary(zh_CN.UTF-8):	ruby - 一种快速高效的面向对象脚本编程语言
Name:		ruby%{ruby_suffix}
Version:	%{basever}.%{patchlevel}
Release:	%{rel}
Epoch:		1
# Public Domain for example for: include/ruby/st.h, strftime.c, ...
License:	(Ruby or BSD) and Public Domain
Group:		Development/Languages
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/2.0/%{oname}-%{basever}-p%{patchlevel}.tar.bz2
# Source0-md5:	20eb8f067d20f6b76b7e16cce2a85a55
Source1:	http://www.ruby-doc.org/download/%{oname}-doc-bundle.tar.gz
# Source1-md5:	ad1af0043be98ba1a4f6d0185df63876
Source2:	http://www.ruby-doc.org/downloads/%{oname}_%{doc_version}_stdlib_rdocs.tgz
# Source2-md5:	ec622612428672c432b6f65dd31a84b5
Source3:	http://www.ruby-doc.org/downloads/%{oname}_%{doc_version}_core_rdocs.tgz
# Source3-md5:	1892aadde51d36106c513bced2193dff
Source100:	ftp://ftp.ruby-lang.org/pub/ruby/1.8/%{oname}-1.8.7-p330.tar.gz
# Source100-md5:	50a49edb787211598d08e756e733e42e
Source4:	rdoc.1
Source5:	testrb.1
Patch0:		%{oname}-lib64.patch
Patch1:		%{oname}-ffs.patch
Patch2:		fix-bison-invocation.patch
# http://redmine.ruby-lang.org/issues/5231
#Patch3:		disable-versioned-paths.patch
# TODO: Should be submitted upstream?
#Patch4:		arch-specific-dir.patch
# http://redmine.ruby-lang.org/issues/5281
#Patch5:		site-and-vendor-arch-flags.patch
# Make mkmf verbose by default
Patch6:		mkmf-verbose.patch
Patch7:		strip-ccache.patch
Patch8:		duplicated-paths.patch
Patch9:		DESTDIR.patch
Patch10:	empty-ruby-version.patch
Patch11:	rubygems-2.0.0-binary-extensions.patch
Patch12:	custom-rubygems-location.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	bison >= 1.875
BuildRequires:	db-devel
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-build >= 5.4.10-49
# boostrap needs ruby binary, erb module
%{!?with_bootstrap:BuildRequires:	ruby-modules}
%{!?with_bootstrap:BuildRequires:	ruby}
BuildRequires:	sed >= 4.0
BuildRequires:	yaml-devel
%if %{with tk}
BuildRequires:	tk-devel
%endif
Requires(post,postun):	/sbin/ldconfig
Provides:	ruby(ver) = %{ruby_version}
Obsoletes:	ruby-REXML <= 2.4.0-2
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread <= 0.6.3
Conflicts:	ruby-activesupport < 2.3.11-2
Conflicts:	ruby-activesupport2 < 2.3.11-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	ruby_ridir		%{_datadir}/ri/%{ruby_version}/system
#%define	gem_dir			%{_datadir}/gems
#%define	gem_dir			%{_datadir}/%{oname}/gems/%{ruby_version}
%define	gem_dir			%{_datadir}/%{oname}/%{ruby_version}/gems

# The RubyGems library has to stay out of Ruby directory three, since the
# RubyGems should be share by all Ruby implementations.
%define	rubygems_dir		%{_datadir}/rubygems

%define	ruby_archdir		%{_libdir}/%{oname}/%{ruby_version}
%define	ruby_libarchdir		%{_libdir}/%{oname}/%{ruby_version}
%define	ruby_libdir		%{_datadir}/%{oname}/%{ruby_version}

# This is the local lib/arch and should not be used for packaging.
%define	sitedir			site_ruby
%define	ruby_sitedir		%{_prefix}/local/share/%{oname}/%{sitedir}
%define	ruby_sitearchdir	%{_prefix}/local/%{_lib}/%{oname}/%{sitedir}/%{ruby_version}
%define	ruby_sitelibdir		%{_prefix}/local/share/%{oname}/%{sitedir}/%{ruby_version}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the PLD repositories.
%define	vendordir		vendor_ruby
%define	ruby_vendordir		%{_datadir}/%{oname}/%{vendordir}
%define	ruby_vendorarchdir	%{_libdir}/%{oname}/%{vendordir}/%{ruby_version}
%define	ruby_vendorlibdir	%{_datadir}/%{oname}/%{vendordir}/%{ruby_version}

# TODO: drop legacy loadpaths after all ruby modules rebuilt in Th
%define	legacy_libdir		%{_libdir}/%{oname}/%{ruby_version}
%define	legacy_archdir		%{_libdir}/%{oname}/%{ruby_version}/%{_target_cpu}-linux
%define	legacy_sitedir		%{_libdir}/%{oname}/%{sitedir}
%define	legacy_sitelibdir	%{_libdir}/%{oname}/%{sitedir}/%{ruby_version}
%define	legacy_sitearchdir	%{_libdir}/%{oname}/%{sitedir}/%{ruby_version}/%{_target_cpu}-linux
%define	legacy_vendordir	%{_libdir}/%{oname}/%{vendordir}
%define	legacy_vendorlibdir	%{_libdir}/%{oname}/%{vendordir}/%{ruby_version}
%define	legacy_vendorarchdir	%{_libdir}/%{oname}/%{vendordir}/%{ruby_version}/%{_target_cpu}-linux

%define	legacy_siteloadpath	%{legacy_sitelibdir}\\0%{legacy_sitearchdir}\\0%{legacy_sitedir}
%define	legacy_vendorloadpath	%{legacy_vendorarchdir}
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
Suggests:	ruby-rubygems
Provides:	ruby-bigdecimal = %{bigdecimal_ver}
Provides:	ruby-io-console = %{io_console_ver}
# ruby-modules deprecated, rpm5 generates ruby(abi) itself
Provides:	ruby-modules(ver) = %{ruby_version}
%if %{with batteries}
Provides:	ruby-minitest = %{minitest_ver}
Obsoletes:	ruby-minitest <= 1.5.0
%endif
# FIXME later
Provides:	ruby(abi) = %{ruby_version}

%description modules
Ruby standard modules and utilities:
- erb - Tiny eRuby
- testrb - automatic runner for Test::Unit of Ruby

%description modules -l pl.UTF-8
Standardowe moduły i narzędzia Ruby:
- erb - mały eRuby
- testrb - automatyczny runner dla Ruby Test::Unit

%package tk
Summary:	Ruby/Tk bindings
Summary(pl.UTF-8):	Wiązania Ruby/Tk
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}

%description tk
This package contains Ruby/Tk bindings.

%description tk -l pl.UTF-8
Ten pakiet zawiera wiązania Ruby/Tk.

%package devel
Summary:	Ruby development libraries
Summary(pl.UTF-8):	Biblioteki programistyczne interpretera języka Ruby
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}
Requires:	gcc
Requires:	glibc-devel
Requires:	pkgconfig

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

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
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc-ri
Ruby ri documentation.

%description doc-ri -l pl.UTF-8
Dokumentacja Ruby w formacie ri.

%package examples
Summary:	Ruby examples
Summary(pl.UTF-8):	Przykłady dla języka Ruby
Group:		Development/Languages
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description examples
Ruby examples.

%description examples -l pl.UTF-8
Przykłady programów w języku Ruby.

# IMPORTANT: keep irb, rdoc, rubygems, rake, json as last packages as we reset epoch/version/release
# and %{version},%{release} macros may not be used directly as they take last
# subpackage value not main package one what you intend to use

%package irb
Summary:	The Interactive Ruby
Version:	%{irb_ver}
Release:	%{basever}.%{patchlevel}.%{rel}
Epoch:		0
Group:		Development/Languages
Requires:	%{name}-modules = 1:%{basever}.%{patchlevel}-%{rel}
Provides:	irb = %{version}-%{release}
Provides:	ruby(irb) = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description irb
The irb is acronym for Interactive Ruby. It evaluates ruby expression
from the terminal.

%package rdoc
Summary:	A tool to generate HTML and command-line documentation for Ruby projects
Summary(pl.UTF-8):	Narzędzie do generowania dokumentacji HTML i linii poleceń dla projektów w Rubym
Version:	%{rdoc_ver}
Release:	%{basever}.%{patchlevel}.%{rel}
Epoch:		0
License:	GPL v2 and Ruby and MIT
Group:		Development/Libraries
Requires:	%{name}-modules = 1:%{basever}.%{patchlevel}-%{rel}
Obsoletes:	rdoc <= 0.9.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description rdoc
RDoc produces HTML and command-line documentation for Ruby projects.
RDoc includes the 'rdoc' and 'ri' tools for generating and displaying
online documentation.

%description rdoc -l pl.UTF-8
RDoc tworzy dokumentację HTML i linii poleceń dla projektów w języku
Ruby. RDoc zawiera narzędzia 'rdoc' i 'ri' do generowania i
wyświetlania dokumentacji online.

%package rubygems
Summary:	RubyGems - the Ruby standard for packaging Ruby libraries
Summary(pl.UTF-8):	RubyGems - standard Ruby'ego pakietowania bibliotek
Version:	%{rubygems_ver}
Release:	%{basever}.%{patchlevel}.%{rel}
Epoch:		0
License:	Ruby or MIT
Group:		Development/Libraries
Requires:	%{name}-modules = 1:%{basever}.%{patchlevel}-%{rel}
Requires:	%{name}-rdoc >= %{rdoc_ver}
Suggests:	%{name}-devel
Provides:	rubygems = %{rubygems_ver}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%description rubygems -l pl.UTF-8
RubyGems to standardowe narzędzie języka Ruby do publikowania i
zarządzania zewnętrznymi bibliotekami.

%package rake
Summary:	Rake is a Make-like program implemented in Ruby
Summary(pl.UTF-8):	Program typu Make dla języka Ruby
Version:	%{rake_ver}
Release:	%{basever}.%{patchlevel}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Languages
Provides:	rake = %{rake_ver}
Conflicts:	ruby-modules < 1:1.9.3.429-2
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description rake
Rake is a simple Ruby build program with capabilities similar to make.

It has the following features:
- Rakefiles (rake's version of Makefiles) are completely defined in
  standard Ruby syntax. No XML files to edit. No quirky Makefile syntax
  to worry about (is that a tab or a space?)
- Users can specify tasks with prerequisites.
- Rake supports rule patterns to synthesize implicit tasks.
- Rake is lightweight. It can be distributed with other projects as a
  single file. Projects that depend upon rake do not require that rake
  be installed on target systems.

%description rake -l pl.UTF-8
Rake to prosty program do budowania w języku Ruby o możliwościach
podobnych do make.

Ma następujące cechy:
- Pliki Rakefile (rake'owa odmiana plików Makefile) są definiowane
  całkowicie w standardowej składni języka Ruby. Nie trzeba modyfikować
  plików XML. Nie trzeba martwić się kaprysami składni Makefile (czy to
  tabulacja czy spacja?).
- Użytkownicy mogą określać zadania z ich zależnościami.
- Rake obsługuje wzorce reguł do tworzenia z nich wynikowych zadań.
- Rake jest lekki. Może być rozpowszechniany z innymi projektami jako
  pojedynczy plik. Projekty używające rake'a nie wymagają go
  zainstalowanego na systemach docelowych.

%package json
Summary:	JSON library for Ruby
Summary(pl.UTF-8):	Biblioteka JSON dla języka Ruby
Version:	%{json_ver}
Release:	%{basever}.%{patchlevel}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Languages
Obsoletes:	ruby-json-rubyforge
Conflicts:	ruby-modules < 1:1.9.3.429-3

%description json
This is a JSON implementation as a Ruby extension in C.

%description json -l pl.UTF-8
Biblioteka JSON dla języka Ruby.

%prep
%if %{with bootstrap}
%setup -q -n %{oname}-%{basever}-p%{patchlevel} -a1 -a2 -a3 -a100
%else
%setup -q -n %{oname}-%{basever}-p%{patchlevel} -a1 -a2 -a3
%endif
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1
#%patch4 -p1
#%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1

# must be regenerated with new bison
%{__rm} parse.{c,h}

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

find -type f '(' -name '*.rb' -o -name '*.cgi' -o -name '*.test' \
	-o -name 'ruby.1' -o -name '*.html' -o -name '*.tcl' ')' \
	| xargs %{__sed} -i 's,/usr/local/bin/,%{_bindir}/,'

%build
rubygems_ver=$(awk '/VERSION =/ && $1 == "VERSION" {print $3}' lib/rubygems.rb | xargs)
if [ $rubygems_ver != %{rubygems_ver} ]; then
	echo "Set %%define rubygems_ver to $rubygems_ver and re-run."
	exit 1
fi
rdoc_ver=$(awk '/VERSION =/ && $1 == "VERSION" {print $3}' lib/rdoc.rb | xargs)
if [ $rdoc_ver != %{rdoc_ver} ]; then
	echo "Set %%define rdoc_ver to $rdoc_ver and re-run."
	exit 1
fi

cp -f /usr/share/automake/config.sub .

# build ruby-1.8.7 first
%if %{with bootstrap}
cd %{oname}-1.8.7-p330
%configure
%{__make}
cd ..
%endif

%{__autoconf}
%configure \
	%{?with_bootstrap:--with-baseruby=%{oname}-1.8.7-p330/miniruby} \
	--program-suffix=%{ruby_suffix} \
	--with-rubygemsdir=%{rubygems_dir} \
	--with-rubylibprefix=%{ruby_libdir} \
	--with-rubyarchprefix=%{ruby_archdir} \
	--with-sitedir=%{ruby_sitelibdir} \
	--with-sitearchdir=%{ruby_sitearchdir} \
	--with-vendordir=%{ruby_vendorlibdir} \
	--with-vendorarchdir=%{ruby_vendorarchdir} \
	--with-rubyhdrdir=%{_includedir}/%{oname}-%{ruby_version} \
	--with-rubyarchhdrdir=%{_includedir}/%{oname}-%{ruby_version} \
	--with-sitearchhdrdir='$(sitehdrdir)/$(arch)' \
	--with-vendorarchhdrdir='$(vendorhdrdir)/$(arch)' \
	--enable-shared \
	--enable-pthread \
	--enable-multiarch \
	--disable-rubygems \
	--disable-install-doc \
	--with-ruby-version=''

%{__make} -j1 main \
	COPY="cp -p" Q= \
	%{?with_bootstrap:BASERUBY="%{oname}-1.8.7-p330/miniruby -I./ruby-1.8.7-p330/lib"}

%if %{with doc}
%{__make} -j1 rdoc
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{basever}.%{patchlevel} \
	$RPM_BUILD_ROOT%{ruby_ridir} \

#install -d $RPM_BUILD_ROOT{%{ruby_rdocdir},%{_examplesdir}/%{oname}-%{version}} \
#	$RPM_BUILD_ROOT{%{ruby_vendorarchdir},%{ruby_ridir}} \
#	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/net \
#	$RPM_BUILD_ROOT%{ruby_vendordir}/data \

#	$RPM_BUILD_ROOT{%{legacy_archdir}/racc,%{legacy_sitelibdir},%{legacy_sitearchdir},%{legacy_vendorarchdir},%{legacy_libdir}/tasks} \

%{__make} install %{?with_doc:install-doc} \
	DESTDIR=$RPM_BUILD_ROOT

cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{basever}.%{patchlevel}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/rdoc%{ruby_suffix}.1
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/testrb%{ruby_suffix}.1

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/html

ln -sf %{gem_dir}/gems/rake-%{rake_ver}/bin/rake $RPM_BUILD_ROOT%{_bindir}/rake%{ruby_suffix}

%if %{without batteries}
# packaged separately
%{__rm} -r $RPM_BUILD_ROOT%{ruby_libdir}/{rubygems,rake,json,minitest}
%{__rm} -r $RPM_BUILD_ROOT%{ruby_archdir}/json
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/rake-*
%{__rm} $RPM_BUILD_ROOT%{ruby_libdir}/{rake,rubygems,json}.rb
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{gem,rake}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/rake*
%{__rm} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/{json,minitest,rake}-*.gemspec
%{?with_doc:%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ri/%{ruby_version}/system/JSON}
%endif

%if %{with doc}
# too much .ri
#%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/cache.ri
#%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/created.rid
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS LEGAL README README.EXT ChangeLog
%attr(755,root,root) %{_bindir}/ruby%{ruby_suffix}
%attr(755,root,root) %{_libdir}/libruby.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libruby.so.%{ruby_version}
%{_mandir}/man1/ruby%{ruby_suffix}.1*

%dir %{_libdir}/%{oname}
%dir %{_libdir}/%{oname}/%{vendordir}
%dir %{_datadir}/%{oname}

%dir %{ruby_libdir}
%dir %{ruby_archdir}
%dir %{ruby_vendordir}
#%dir %{ruby_vendordir}/data
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorarchdir}

#%dir %{_datadir}/ri
#%dir %{_datadir}/ri/%{ruby_version}
%dir %{ruby_ridir}

#%dir %{ruby_rdocdir}

# common dirs for ruby vendor modules
#%dir %{ruby_vendorlibdir}/net

# legacy dirs. when everything rebuilt in Th not using these dirs. drop them
%if 0
%dir %{legacy_archdir}
%dir %{legacy_sitedir}
%dir %{legacy_sitelibdir}
%dir %{legacy_sitearchdir}
%dir %{legacy_vendorarchdir}
%dir %{legacy_libdir}/tasks
%dir %{legacy_archdir}/racc
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libruby.so
%{_includedir}/%{oname}-%{ruby_version}
%{_pkgconfigdir}/ruby-%{ruby_version}.pc
%{ruby_libdir}/mkmf.rb

%files static
%defattr(644,root,root,755)
%{_libdir}/libruby-static.a

%if %{with tk}
%files tk
%defattr(644,root,root,755)
%{ruby_libdir}/tcltk.rb
%{ruby_libdir}/tk*.rb
%{ruby_libdir}/tk
%{ruby_libdir}/tkextlib
%attr(755,root,root) %{ruby_archdir}/t*.so
%endif

%files irb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/irb%{ruby_suffix}
%{ruby_libdir}/irb.rb
%{ruby_libdir}/irb
%{_mandir}/man1/irb%{ruby_suffix}.1*

%files rdoc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdoc%{ruby_suffix}
%attr(755,root,root) %{_bindir}/ri%{ruby_suffix}
%{_mandir}/man1/rdoc%{ruby_suffix}.1*
%{ruby_libdir}/rdoc
%dir %{gem_dir}/gems/rdoc-%{rdoc_ver}
%dir %{gem_dir}/gems/rdoc-%{rdoc_ver}/bin
%attr(755,root,root) %{gem_dir}/gems/rdoc-%{rdoc_ver}/bin/rdoc
%{gem_dir}/specifications/default/rdoc-%{rdoc_ver}.gemspec
%attr(755,root,root) %{gem_dir}/gems/rdoc-%{rdoc_ver}/bin/ri

%if %{with batteries}
%files rubygems
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gem%{ruby_suffix}
%dir %{rubygems_dir}
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb
%{rubygems_dir}/ubygems.rb
%{rubygems_dir}/rbconfig

%files rake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rake%{ruby_suffix}
%{_mandir}/man1/rake%{ruby_suffix}.1*
%{ruby_libdir}/rake
%dir %{gem_dir}/gems/rake-%{rake_ver}
%dir %{gem_dir}/gems/rake-%{rake_ver}/bin
%attr(755,root,root) %{gem_dir}/gems/rake-%{rake_ver}/bin/rake
%{gem_dir}/specifications/default/rake-%{rake_ver}.gemspec

%files json
%defattr(644,root,root,755)
%{ruby_libdir}/json
%dir %{ruby_archdir}/json
%dir %{ruby_archdir}/json/ext
%attr(755,root,root) %{ruby_archdir}/json/ext/*.so
%{gem_dir}/specifications/default/json-%{json_ver}.gemspec
%endif

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erb%{ruby_suffix}
%attr(755,root,root) %{_bindir}/testrb%{ruby_suffix}
%{ruby_libdir}/bigdecimal
%{ruby_libdir}/cgi
%{ruby_libdir}/date
%{ruby_libdir}/digest
%{ruby_libdir}/dl
%{ruby_libdir}/drb
%{ruby_libdir}/fiddle
%{ruby_libdir}/io
%{ruby_libdir}/matrix
%{ruby_libdir}/net
%{ruby_libdir}/openssl
%{ruby_libdir}/optparse
%{ruby_libdir}/psych
%{ruby_libdir}/racc
%{ruby_libdir}/rbconfig
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper
%{ruby_libdir}/rss
%{ruby_libdir}/shell
#%{ruby_libdir}/syck
%{ruby_libdir}/syslog
%{ruby_libdir}/test
%{ruby_libdir}/uri
%{ruby_libdir}/webrick
%{ruby_libdir}/xmlrpc
%{ruby_libdir}/yaml
%{ruby_libdir}/[A-Za-s]*.rb
%{ruby_libdir}/tempfile.rb
%{ruby_libdir}/thread.rb
%{ruby_libdir}/thwait.rb
%{ruby_libdir}/time.rb
%{ruby_libdir}/timeout.rb
%{ruby_libdir}/tmpdir.rb
%{ruby_libdir}/tracer.rb
%{ruby_libdir}/tsort.rb
%{ruby_libdir}/[u-z]*.rb
%if %{with batteries}
#%exclude %{ruby_libdir}/rubygems.rb
#%exclude %{ruby_libdir}/ubygems.rb
%endif
%exclude %{ruby_libdir}/irb.rb
%exclude %{ruby_libdir}/mkmf.rb
%attr(755,root,root) %{ruby_archdir}/[a-s]*.so
%attr(755,root,root) %{ruby_archdir}/[u-z]*.so
%dir %{ruby_archdir}/digest
%attr(755,root,root) %{ruby_archdir}/digest/*.so
%dir %{ruby_archdir}/dl
%attr(755,root,root) %{ruby_archdir}/dl/callback.so
%dir %{ruby_archdir}/enc
%attr(755,root,root) %{ruby_archdir}/enc/*.so
%dir %{ruby_archdir}/enc/trans
%attr(755,root,root) %{ruby_archdir}/enc/trans/*.so
%dir %{ruby_archdir}/io
%attr(755,root,root) %{ruby_archdir}/io/*.so
%dir %{ruby_archdir}/mathn
%attr(755,root,root) %{ruby_archdir}/mathn/*.so
%dir %{ruby_archdir}/racc
%attr(755,root,root) %{ruby_archdir}/racc/*.so
%{ruby_archdir}/rbconfig.rb

%{gem_dir}/specifications/default/bigdecimal-%{bigdecimal_ver}.gemspec
%{gem_dir}/specifications/default/io-console-%{io_console_ver}.gemspec

%if %{with batteries}
# minitest
%{ruby_libdir}/minitest
%{gem_dir}/specifications/default/minitest-%{minitest_ver}.gemspec
%endif

%{gem_dir}/specifications/default/psych-%{psych_ver}.gemspec

# test-unit
%{gem_dir}/specifications/default/test-unit-%{test_unit_ver}.gemspec
%dir %{gem_dir}/gems/test-unit-%{test_unit_ver}
%dir %{gem_dir}/gems/test-unit-%{test_unit_ver}/bin
%attr(755,root,root) %{gem_dir}/gems/test-unit-%{test_unit_ver}/bin/testrb

# parents of gem_dir
#%dir %{_datadir}/%{oname}/gems
#%dir %{_datadir}/%{oname}/gems/%{ruby_version}
#%dir %{_datadir}/%{oname}/gems/%{ruby_version}/gems

%dir %{_datadir}/%{oname}/%{ruby_version}/gems/gems

%dir %{gem_dir}
%dir %{gem_dir}/specifications
%dir %{gem_dir}/specifications/default
%{_mandir}/man1/erb%{ruby_suffix}.1*
%{_mandir}/man1/ri%{ruby_suffix}.1*
%{_mandir}/man1/testrb%{ruby_suffix}.1*

%files doc
%defattr(644,root,root,755)
%doc ruby-doc-bundle/*
%{?with_doc:%doc ruby_%{doc_version}_stdlib}
%{?with_doc:%doc ruby_%{doc_version}_core}

%if %{with doc}
%files doc-ri
%defattr(644,root,root,755)
%{ruby_ridir}/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{oname}-*
