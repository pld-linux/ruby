# TODO:
#	- include ext/ in docs
#	- replace ri with fastri
#	- patch ri to search multiple indexes (one per package), so RPMs can install ri docs
#	- unpackaged /usr/share/gems/specifications/default/openssl-2.0.7.gemspec ?
#
# Conditional build:
%bcond_without	doc		# skip (time-consuming) docs generating; intended for speed up test builds
%bcond_without	batteries	# Don't include rubygems, json, rake, minitest
%bcond_without	default_ruby	# use this Ruby as default system Ruby
%bcond_with	bootstrap	# build bootstrap version
%bcond_with	tests		# build without tests

%define		rel		1
%define		ruby_version	2.4
%define		patchlevel	4
%define		pkg_version	%{ruby_version}.%{patchlevel}
%define		ruby_suffix %{!?with_default_ruby:%{ruby_version}}
%define		doc_version	2_4_3
%define		oname	ruby
Summary:	Ruby - interpreted scripting language
Summary(ja.UTF-8):	オブジェクト指向言語Rubyインタプリタ
Summary(pl.UTF-8):	Ruby - interpretowany język skryptowy
Summary(pt_BR.UTF-8):	Linguagem de script orientada a objeto
Summary(zh_CN.UTF-8):	ruby - 一种快速高效的面向对象脚本编程语言
Name:		ruby%{ruby_suffix}
Version:	%{pkg_version}
Release:	%{rel}
Epoch:		1
# Public Domain for example for: include/ruby/st.h, strftime.c, missing/*, ...
# MIT and CCO: ccan/*
# zlib: ext/digest/md5/md5.*, ext/nkf/nkf-utf8/nkf.c
# UCD: some of enc/trans/**/*.src
License:	(Ruby or BSD) and Public Domain and MIT and CC0 and zlib and UCD
Group:		Development/Languages
# https://www.ruby-lang.org/en/downloads/
Source0:	https://cache.ruby-lang.org/pub/ruby/%{ruby_version}/%{oname}-%{pkg_version}.tar.xz
# Source0-md5:	4f30cefb7d50c6fa4d801f47ed9d82ca
Source2:	http://www.ruby-doc.org/downloads/%{oname}_%{doc_version}_stdlib_rdocs.tgz
# Source2-md5:	d21fb29009644bd174dbba0dad53f1f5
Source3:	http://www.ruby-doc.org/downloads/%{oname}_%{doc_version}_core_rdocs.tgz
# Source3-md5:	3aef8f1b7fb3d140ac9ba8f3061c832e
Source50:	http://www.unicode.org/Public/9.0.0/ucd/CaseFolding.txt
# Source50-md5:	e3fbf2f626f10070000fe66f3a2ff5ef
Source51:	http://www.unicode.org/Public/9.0.0/ucd/CompositionExclusions.txt
# Source51-md5:	263381d7b4b5e2d52a91e1bbbd4722d4
Source52:	http://www.unicode.org/Public/9.0.0/ucd/NormalizationTest.txt
# Source52-md5:	aacb8a8acfc449d09136fe39f3f97cf1
Source53:	http://www.unicode.org/Public/9.0.0/ucd/SpecialCasing.txt
# Source53-md5:	fea30f45a2f81ffa474fd984d297e2ea
Source54:	http://www.unicode.org/Public/9.0.0/ucd/UnicodeData.txt
# Source54-md5:	dde25b1cf9bbb4ba1140ac12e4128b0b
Source100:	ftp://ftp.ruby-lang.org/pub/ruby/1.8/%{oname}-1.8.7-p330.tar.gz
# Source100-md5:	50a49edb787211598d08e756e733e42e
Source4:	rdoc.1
Source5:	testrb.1
Source6:	operating_system.rb
#Patch1:		%{oname}-ffs.patch
Patch2:		fix-bison-invocation.patch
Patch3:		mkmf-verbose.patch
Patch4:		strip-ccache.patch
Patch5:		ruby-version.patch
Patch6:		duplicated-paths.patch
# obsolete?
Patch8:		rubygems-2.0.0-binary-extensions.patch
Patch9:		custom-rubygems-location.patch
Patch12:	archlibdir.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake
BuildRequires:	bison >= 1.875
BuildRequires:	db-devel
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	gmp-devel
BuildRequires:	libffi-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-build >= 5.4.10-49
BuildRequires:	sed >= 4.0
BuildRequires:	systemtap-sdt-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
%if %{without bootstrap}
# bootstrap needs ruby binary, erb module
BuildRequires:	rpm-rubyprov
BuildRequires:	ruby
BuildRequires:	ruby-modules
%endif
Requires(post,postun):	/sbin/ldconfig
Obsoletes:	ruby-REXML <= 2.4.0-2
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread <= 0.6.3
Conflicts:	rpm-build-macros < 1.695
Conflicts:	ruby-activesupport < 2.3.11-2
Conflicts:	ruby-activesupport2 < 2.3.11-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	bigdecimal_ver		1.3.2
%define	io_console_ver		0.4.6
%define	irb_ver			0.9.6
%define	json_ver		2.0.4
%define	minitest_ver		5.10.1
%define	psych_ver		2.2.2
%define	rake_ver		12.0.0
%define	rdoc_ver		5.0.0
%define	rubygems_ver		2.6.14.1
%define	test_unit_ver		3.2.3
%define	power_assert_ver	0.4.1
%define	did_you_mean_ver	1.1.0
%define	net_telnet_ver		0.1.1
%define	xmlrpc_ver		0.2.1

%define	ruby_ridir		%{_datadir}/ri/system
%define	gem_dir			%{_datadir}/gems
%define	gem_libdir		%{_libdir}/gems/%{oname}

# location where rubygems is installed
%define	rubygems_dir		%{ruby_libdir}

%define	ruby_archdir		%{_libdir}/%{oname}/%{ruby_version}
%define	ruby_libarchdir		%{_libdir}/%{oname}/%{ruby_version}
%define	ruby_libdir		%{_datadir}/%{oname}/%{ruby_version}

# This is the local lib/arch and should not be used for packaging.
%define	sitedir			site_ruby
%define	ruby_sitearchdir	%{_prefix}/local/%{_lib}/%{oname}/%{sitedir}/%{ruby_version}
%define	ruby_sitelibdir		%{_prefix}/local/share/%{oname}/%{sitedir}

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the PLD repositories.
%define	vendordir		vendor_ruby
%define	ruby_vendorarchdir	%{_libdir}/%{oname}/%{vendordir}/%{ruby_version}
%define	ruby_vendorlibdir	%{_datadir}/%{oname}/%{vendordir}

# bleh, some nasty (gcc or ruby) bug still not fixed
# (SEGV or "unexpected break" on miniruby run during build)
%define	specflags_ia64	-O0

# ruby needs frame pointers for correct exception handling
%define	specflags_ia32	-fno-omit-frame-pointer

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
# ruby-modules deprecated, rpm5 generates ruby(abi) itself
Provides:	ruby-modules(ver) = %{ruby_version}
# FIXME later
Provides:	ruby(abi) = %{ruby_version}
%requires_ge_to	openssl	openssl-devel

%description modules
Ruby standard modules and utilities:
- erb - Tiny eRuby
- testrb - automatic runner for Test::Unit of Ruby

%description modules -l pl.UTF-8
Standardowe moduły i narzędzia Ruby:
- erb - mały eRuby
- testrb - automatyczny runner dla Ruby Test::Unit

%package devel
Summary:	Ruby development libraries
Summary(pl.UTF-8):	Biblioteki programistyczne interpretera języka Ruby
Group:		Development/Languages
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}
Requires:	gcc
Requires:	glibc-devel
Requires:	gmp-devel
Requires:	pkgconfig

%description devel
Ruby development libraries.

%description devel -l pl.UTF-8
Biblioteki programistyczne interpretera języka Ruby.

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
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Languages
Requires:	%{name}-modules = 1:%{pkg_version}-%{rel}
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
Release:	%{pkg_version}.%{rel}
Epoch:		0
# SIL: lib/rdoc/generator/template/darkfish/css/fonts.css
License:	GPLv2 and Ruby and MIT and SIL
Group:		Development/Libraries
Requires:	%{name}-irb >= %{irb_ver}
Requires:	%{name}-json >= %{json_ver}
Requires:	%{name}-modules = 1:%{pkg_version}-%{rel}
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
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	Ruby or MIT
Group:		Development/Libraries
Requires:	%{name}-bigdecimal = %{bigdecimal_ver}-%{pkg_version}.%{rel}
Requires:	%{name}-io-console = %{io_console_ver}-%{pkg_version}.%{rel}
Requires:	%{name}-modules = 1:%{pkg_version}-%{rel}
Requires:	%{name}-psych = %{psych_ver}-%{pkg_version}.%{rel}
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
Release:	%{pkg_version}.%{rel}
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
Release:	%{pkg_version}.%{rel}
Epoch:		0
# UCD: ext/json/generator/generator.c
License:	(Ruby or GPLv2) and UCD
Group:		Development/Languages
Obsoletes:	ruby-json-rubyforge
Conflicts:	ruby-modules < 1:1.9.3.429-3

%description json
This is a JSON implementation as a Ruby extension in C.

%description json -l pl.UTF-8
Biblioteka JSON dla języka Ruby.

%package minitest
Summary:	Minitest provides a complete suite of testing facilities
Version:	%{minitest_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.

%package power_assert
# The Summary/Description fields are rather poor.
# https://github.com/k-tsj/power_assert/issues/3
Summary:	Power Assert for Ruby
Version:	%{power_assert_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	Ruby or BSD
Group:		Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description power_assert
Power Assert shows each value of variables and method calls in the
expression. It is useful for testing, providing which value wasn't
correct when the condition is not satisfied.

%package test-unit
# The Summary/Description fields are rather poor.
# https://github.com/test-unit/test-unit/issues/73
Summary:	Improved version of Test::Unit bundled in Ruby 1.8.x
Version:	%{test_unit_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Libraries
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:	(Ruby or BSD) and (Ruby or BSD or Python) and (Ruby or BSD or LGPLv2+)
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description test-unit
Ruby 1.9.x bundles minitest not Test::Unit. Test::Unit bundled in Ruby
1.8.x had not been improved but unbundled Test::Unit (test-unit) is
improved actively.

%package did_you_mean
Summary:	"Did you mean?" experience in Ruby
Version:	%{did_you_mean_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description did_you_mean
"did you mean?" experience in Ruby: the error message will tell you
the right one when you misspelled something.

%package net-telnet
Summary:	Provides telnet client functionality
Version:	%{net_telnet_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description net-telnet
Provides telnet client functionality.

This class also has, through delegation, all the methods of a socket
object (by default, a TCPSocket, but can be set by the Proxy option to
new()). This provides methods such as close() to end the session and
sysread() to read data directly from the host, instead of via the
waitfor() mechanism. Note that if you do use sysread() directly when
in telnet mode, you should probably pass the output through
preprocess() to extract telnet command sequences.

%package bigdecimal
Summary:	BigDecimal provides arbitrary-precision floating point decimal arithmetic
Version:	%{bigdecimal_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	GPL+ or Artistic
Group:		Development/Libraries

%description bigdecimal
Ruby provides built-in support for arbitrary precision integer
arithmetic. For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate
floating point numbers. Decimal arithmetic is also useful for general
calculation, because it provides the correct answers people
expect–whereas normal binary floating point arithmetic often
introduces subtle errors because of the conversion between base 10 and
base 2.

%package io-console
Summary:	IO/Console is a simple console utilizing library
Version:	%{io_console_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Libraries

%description io-console
IO/Console provides very simple and portable access to console. It
doesn't provide higher layer features, such like curses and readline.

%package psych
Summary:	A libyaml wrapper for Ruby
Version:	%{psych_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries

%description psych
Psych is a YAML parser and emitter. Psych leverages libyaml for its
YAML parsing and emitting capabilities. In addition to wrapping
libyaml, Psych also knows how to serialize and de-serialize most Ruby
objects to and from the YAML format.

%package xmlrpc
Summary:	A xmlrpc wrapper for Ruby
Version:	%{xmlrpc_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries

%description xmlrpc
XMLRPC is a lightweight protocol that enables remote procedure calls
over HTTP.  It is defined at http://www.xmlrpc.com.

XMLRPC allows you to create simple distributed computing solutions
that span computer languages.  Its distinctive feature is its
simplicity compared to other approaches like SOAP and CORBA.

The Ruby standard library package 'xmlrpc' enables you to create a
server that implements remote procedures and a client that calls them.
Very little code is required to achieve either of these.

%prep
%setup -q -n %{oname}-%{pkg_version} -a2 -a3 %{?with_bootstrap:-a100}
#%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
#%patch8 -p1
%patch9 -p1
%patch12 -p1

# must be regenerated with new bison
%{__rm} parse.{c,h}

# Remove bundled libraries to be sure they are not used.
%{__rm} -r ext/psych/yaml
%{__rm} -r ext/fiddle/libffi*

# Install custom operating_system.rb.
install -d lib/rubygems/defaults
cp -p %{SOURCE6} lib/rubygems/defaults

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
	--with-archlibdir=%{_libdir} \
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
	--enable-multiarch \
	--enable-shared \
	--disable-install-doc \
	--disable-rpath \
	--disable-rubygems \
	--with-ruby-version='' \

%{__make} -j1 main \
	COPY="cp -p" Q= \
	%{?with_bootstrap:BASERUBY="%{oname}-1.8.7-p330/miniruby -I./ruby-1.8.7-p330/lib"}

%if %{with doc}
%{__make} -j1 rdoc
%endif

%if %{with tests}
# unset these, as testsuite does "git commit" somewhere, which points to pld .spec repo. doh
unset GIT_DIR GIT_WORK_TREE

unset GIT
DISABLE_TESTS=""

%ifarch armv7l armv7hl armv7hnl
# test_call_double(DL::TestDL) fails on ARM HardFP
# http://bugs.ruby-lang.org/issues/6592
DISABLE_TESTS="-x test_dl2.rb $DISABLE_TESTS"
%endif

# test_debug(TestRubyOptions) fails due to LoadError reported in debug mode,
# when abrt.rb cannot be required (seems to be easier way then customizing
# the test suite).
touch abrt.rb

# TestSignal#test_hup_me hangs up the test suite.
# http://bugs.ruby-lang.org/issues/8997
sed -i '/def test_hup_me/,/end if Process.respond_to/ s/^/#/' test/ruby/test_signal.rb

# Fix "Could not find 'minitest'" error.
# http://bugs.ruby-lang.org/issues/9259
sed -i "/^  gem 'minitest', '~> 4.0'/ s/^/#/" lib/rubygems/test_case.rb

# Segmentation fault.
# https://bugs.ruby-lang.org/issues/9198
sed -i '/^  def test_machine_stackoverflow/,/^  end/ s/^/#/' test/ruby/test_exception.rb

# Don't test wrap ciphers to prevent "OpenSSL::Cipher::CipherError: wrap mode
# not allowed" error.
# https://bugs.ruby-lang.org/issues/10229
sed -i '/assert(OpenSSL::Cipher::Cipher.new(name).is_a?(OpenSSL::Cipher::Cipher))/i \
        next if /wrap/ =~ name' test/openssl/test_cipher.rb

# Test is broken due to SSLv3 disabled in Fedora.
# https://bugs.ruby-lang.org/issues/10046
sed -i '/def test_ctx_server_session_cb$/,/^  end$/ s/^/#/' test/openssl/test_ssl_session.rb

%{__make} check TESTS="-v $DISABLE_TESTS"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir},%{ruby_ridir}} \
	$RPM_BUILD_ROOT%{ruby_vendorarchdir} \
	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/net \
	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/data \

%{__make} install %{?with_doc:install-doc -j1} \
	DESTDIR=$RPM_BUILD_ROOT

# Version is empty if --with-ruby-version is specified.
# http://bugs.ruby-lang.org/issues/7807
sed -i -e 's/Version: \${ruby_version}/Version: %{ruby_version}/' $RPM_BUILD_ROOT%{_pkgconfigdir}/%{oname}-%{ruby_version}.pc

# Kill bundled certificates, as they should be part of ca-certificates.
for cert in \
	AddTrustExternalCARoot.pem \
	DigiCertHighAssuranceEVRootCA.pem \
	GlobalSignRootCA.pem \
; do
	%{__rm} $RPM_BUILD_ROOT%{rubygems_dir}/rubygems/ssl_certs/*/$cert
done

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}
cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1/rdoc%{ruby_suffix}.1
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/testrb%{ruby_suffix}.1

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/html

# detect this runtime, "make install" is affected by operating_system.rb what is installed in system!
gem_dir=$(./miniruby -Ilib -I. -I.ext/common ./tool/runruby.rb -- --disable-gems -r$(basename *-linux*-fake.rb .rb) -r rubygems -e 'puts Gem.default_dir')

# Move gems root into common directory, out of Ruby directory structure.
install -d $RPM_BUILD_ROOT%{gem_dir}
%{__mv} $RPM_BUILD_ROOT${gem_dir}/{gems,specifications} $RPM_BUILD_ROOT%{gem_dir}

# Move bundled rubygems to %gem_dir
# make symlinks for io-console and bigdecimal, which are considered to be part of stdlib by other Gems
# make symlinks for all packages, so they would work without rubygems
# NOTE: when making symlinks, do not symlink paths that could be directories,
# as there may came files from other packages as well. actually, unlikely as
# the links to got system dir and only ruby may package there (other distro
# packages should go to vendor dirs)
%if 0
install -d $RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/rake* $RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/lib
ln -s %{gem_dir}/gems/rake-%{rake_ver}/lib/rake $RPM_BUILD_ROOT%{ruby_libdir}
ln -s %{gem_dir}/gems/rake-%{rake_ver}/lib/rake.rb $RPM_BUILD_ROOT%{ruby_libdir}
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/rake-%{rake_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
%endif

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/rdoc-%{rdoc_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/rdoc* $RPM_BUILD_ROOT%{gem_dir}/gems/rdoc-%{rdoc_ver}/lib
ln -s %{gem_dir}/gems/rdoc-%{rdoc_ver}/lib/rdoc $RPM_BUILD_ROOT%{ruby_libdir}
ln -s %{gem_dir}/gems/rdoc-%{rdoc_ver}/lib/rdoc.rb $RPM_BUILD_ROOT%{ruby_libdir}
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/rdoc-%{rdoc_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/bigdecimal-%{bigdecimal_ver}/lib
install -d $RPM_BUILD_ROOT%{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/bigdecimal $RPM_BUILD_ROOT%{gem_dir}/gems/bigdecimal-%{bigdecimal_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal.so $RPM_BUILD_ROOT%{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/bigdecimal-%{bigdecimal_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal $RPM_BUILD_ROOT%{ruby_libdir}/bigdecimal
ln -s %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal.so $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal.so

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/io-console-%{io_console_ver}/lib
install -d $RPM_BUILD_ROOT%{gem_libdir}/io-console-%{io_console_ver}/lib/io
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/io $RPM_BUILD_ROOT%{gem_dir}/gems/io-console-%{io_console_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/io/console.so $RPM_BUILD_ROOT%{gem_libdir}/io-console-%{io_console_ver}/lib/io
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/io-console-%{io_console_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/io-console-%{io_console_ver}/lib/io $RPM_BUILD_ROOT%{ruby_libdir}/io
ln -s %{gem_libdir}/io-console-%{io_console_ver}/lib/io/console.so $RPM_BUILD_ROOT%{ruby_libarchdir}/io/console.so

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/json-%{json_ver}/lib
install -d $RPM_BUILD_ROOT%{gem_libdir}/json-%{json_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/json* $RPM_BUILD_ROOT%{gem_dir}/gems/json-%{json_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/json $RPM_BUILD_ROOT%{gem_libdir}/json-%{json_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/json-%{json_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/json-%{json_ver}/lib/json $RPM_BUILD_ROOT%{ruby_libdir}/json
ln -s %{gem_dir}/gems/json-%{json_ver}/lib/json.rb $RPM_BUILD_ROOT%{ruby_libdir}/json.rb
install -d $RPM_BUILD_ROOT%{ruby_libarchdir}/json/ext
ln -s %{gem_libdir}/json-%{json_ver}/lib/json/ext/parser.so $RPM_BUILD_ROOT%{ruby_libarchdir}/json/ext
ln -s %{gem_libdir}/json-%{json_ver}/lib/json/ext/generator.so $RPM_BUILD_ROOT%{ruby_libarchdir}/json/ext

ln -s %{gem_dir}/gems/minitest-%{minitest_ver}/lib/minitest $RPM_BUILD_ROOT%{ruby_libdir}

install -d $RPM_BUILD_ROOT%{ruby_libdir}/test
ln -s %{gem_dir}/gems/test-unit-%{test_unit_ver}/lib/unit $RPM_BUILD_ROOT%{ruby_libdir}/test

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/psych-%{psych_ver}/lib
install -d $RPM_BUILD_ROOT%{gem_libdir}/psych-%{psych_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/psych* $RPM_BUILD_ROOT%{gem_dir}/gems/psych-%{psych_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/psych.so $RPM_BUILD_ROOT%{gem_libdir}/psych-%{psych_ver}/lib/
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/psych-%{psych_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/psych-%{psych_ver}/lib/psych $RPM_BUILD_ROOT%{ruby_libdir}/psych
ln -s %{gem_dir}/gems/psych-%{psych_ver}/lib/psych.rb $RPM_BUILD_ROOT%{ruby_libdir}/psych.rb
ln -s %{gem_libdir}/psych-%{psych_ver}/lib/psych.so $RPM_BUILD_ROOT%{ruby_archdir}/psych.so

# Adjust the gemspec files so that the gems will load properly
sed -i '/^end$/ i\
  s.require_paths = ["lib"]' $RPM_BUILD_ROOT%{gem_dir}/specifications/rake-%{rake_ver}.gemspec

sed -i '/^end$/ i\
  s.require_paths = ["lib"]' $RPM_BUILD_ROOT%{gem_dir}/specifications/rdoc-%{rdoc_ver}.gemspec

sed -i '/^end$/ i\
  s.require_paths = ["lib"]\
  s.extensions = ["bigdecimal.so"]' $RPM_BUILD_ROOT%{gem_dir}/specifications/bigdecimal-%{bigdecimal_ver}.gemspec

sed -i '/^end$/ i\
  s.require_paths = ["lib"]\
  s.extensions = ["io/console.so"]' $RPM_BUILD_ROOT%{gem_dir}/specifications/io-console-%{io_console_ver}.gemspec

sed -i '/^end$/ i\
  s.require_paths = ["lib"]\
  s.extensions = ["json/ext/parser.so", "json/ext/generator.so"]' $RPM_BUILD_ROOT%{gem_dir}/specifications/json-%{json_ver}.gemspec

sed -i '/^end$/ i\
  s.require_paths = ["lib"]' $RPM_BUILD_ROOT%{gem_dir}/specifications/minitest-%{minitest_ver}.gemspec

# Push the .gemspecs through the RubyGems to let them write the stub headers.
# This speeds up loading of libraries and avoids warnings in Spring:
# https://github.com/rubygems/rubygems/pull/694
for s in rake-%{rake_ver}.gemspec rdoc-%{rdoc_ver}.gemspec json-%{json_ver}.gemspec; do
	s="$RPM_BUILD_ROOT%{gem_dir}/specifications/$s"
	%{__make} runruby TESTRUN_SCRIPT="-rubygems \
	-e \"spec = Gem::Specification.load('$s')\" \
	-e \"File.write '$s', spec.to_ruby\""
done

ln -sf %{gem_dir}/gems/rake-%{rake_ver}/exe/rake $RPM_BUILD_ROOT%{_bindir}/rake%{ruby_suffix}

%{__sed} -i -e '1s,/usr/bin/env ruby,/usr/bin/ruby,' \
	$RPM_BUILD_ROOT%{ruby_libdir}/abbrev.rb \
	$RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/bin/console \
	$RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/exe/rake \
	$RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}/{cal,test,time,uumerge}.rb \
	$RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}/{drb,logger,openssl,ripper,rss}/*.rb \
	$RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}/webrick/*.cgi

# gem non library files
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/minitest-%{minitest_ver}/test
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/test-unit-%{test_unit_ver}/{[A-Z]*,doc,sample,test}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/power_assert-%{power_assert_ver}/{[A-Z]*,test}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/did_you_mean-%{did_you_mean_ver}/{[A-Z]*,doc,test}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/{[A-Z]*,doc}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/net-telnet-%{net_telnet_ver}/{[A-Z]*,bin}

%if %{without batteries}
# packaged separately
%{__rm} -r $RPM_BUILD_ROOT%{ruby_libdir}/{rubygems,rake,json,minitest}
%{__rm} -r $RPM_BUILD_ROOT%{ruby_archdir}/json
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/rake-*
%{__rm} $RPM_BUILD_ROOT%{ruby_libdir}/{rake,rubygems,json}.rb
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{gem,rake}
#%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/rake*
%{__rm} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/{json,minitest,rake}-*.gemspec
%{?with_doc:%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/ri/%{ruby_version}/system/JSON}
%endif

%if %{with doc}
# too much .ri
%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/cache.ri
%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/created.rid
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc NEWS LEGAL BSDL README.md README.EXT ChangeLog
%attr(755,root,root) %{_bindir}/ruby%{ruby_suffix}
%attr(755,root,root) %{_libdir}/libruby.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libruby.so.%{ruby_version}
%{_mandir}/man1/ruby%{ruby_suffix}.1*

%dir %{_libdir}/%{oname}
%dir %{_libdir}/%{oname}/%{vendordir}
%dir %{_datadir}/%{oname}

%dir %{ruby_libdir}
%dir %{ruby_archdir}
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorarchdir}

%dir %{dirname:%{ruby_ridir}}
%dir %{ruby_ridir}
%dir %{ruby_rdocdir}

# common dirs for ruby vendor modules
%dir %{ruby_vendorlibdir}/data
%dir %{ruby_vendorlibdir}/net

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libruby.so
%{_includedir}/%{oname}-%{ruby_version}
%{_pkgconfigdir}/%{oname}-%{ruby_version}.pc
%{ruby_libdir}/mkmf.rb

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
%{gem_dir}/gems/rdoc-%{rdoc_ver}/lib
%{gem_dir}/specifications/rdoc-%{rdoc_ver}.gemspec
%dir %{gem_dir}/gems/rdoc-5.0.0/exe
%{gem_dir}/gems/rdoc-5.0.0/exe/rdoc
%{gem_dir}/gems/rdoc-5.0.0/exe/ri

%if %{with batteries}
%files rubygems
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gem%{ruby_suffix}
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb
%{rubygems_dir}/ubygems.rb
%{rubygems_dir}/rbconfig

%files rake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rake%{ruby_suffix}
%dir %{gem_dir}/gems/rake-%{rake_ver}
%{gem_dir}/gems/rake-%{rake_ver}/lib
%dir %{gem_dir}/gems/rake-%{rake_ver}/bin
%attr(755,root,root) %{gem_dir}/gems/rake-%{rake_ver}/bin/console
%attr(755,root,root) %{gem_dir}/gems/rake-%{rake_ver}/bin/setup
%{gem_dir}/specifications/rake-%{rake_ver}.gemspec
%{gem_dir}/gems/rake-%{rake_ver}/appveyor.yml
%dir %{gem_dir}/gems/rake-%{rake_ver}/exe
%{gem_dir}/gems/rake-%{rake_ver}/exe/rake

%files json
%defattr(644,root,root,755)
%{ruby_libdir}/json
%dir %{ruby_archdir}/json
%dir %{ruby_archdir}/json/ext
%attr(755,root,root) %{ruby_archdir}/json/ext/*.so

%dir %{gem_libdir}/json-%{json_ver}
%dir %{gem_libdir}/json-%{json_ver}/lib
%dir %{gem_libdir}/json-%{json_ver}/lib/json
%dir %{gem_libdir}/json-%{json_ver}/lib/json/ext
%attr(755,root,root) %{gem_libdir}/json-%{json_ver}/lib/json/ext/generator.so
%attr(755,root,root) %{gem_libdir}/json-%{json_ver}/lib/json/ext/parser.so

%{gem_dir}/gems/json-%{json_ver}
%{gem_dir}/specifications/json-%{json_ver}.gemspec
%endif

%files power_assert
%defattr(644,root,root,755)
%dir %{gem_dir}/gems/power_assert-%{power_assert_ver}
%{gem_dir}/gems/power_assert-%{power_assert_ver}/lib
%{gem_dir}/specifications/power_assert-%{power_assert_ver}.gemspec
%dir %{gem_dir}/gems/power_assert-0.4.1/benchmarks
%{gem_dir}/gems/power_assert-0.4.1/benchmarks/bm_yhpg.rb
%{gem_dir}/gems/power_assert-0.4.1/benchmarks/helper.rb

%files minitest
%defattr(644,root,root,755)
%{ruby_libdir}/minitest
%{gem_dir}/gems/minitest-%{minitest_ver}
%{gem_dir}/specifications/minitest-%{minitest_ver}.gemspec

%files test-unit
%defattr(644,root,root,755)
%dir %{gem_dir}/gems/test-unit-%{test_unit_ver}
%{gem_dir}/gems/test-unit-%{test_unit_ver}/lib
%{gem_dir}/specifications/test-unit-%{test_unit_ver}.gemspec
%{_mandir}/man1/testrb%{ruby_suffix}.1*

%files did_you_mean
%defattr(644,root,root,755)
%dir %{gem_dir}/gems/did_you_mean-%{did_you_mean_ver}
%{gem_dir}/gems/did_you_mean-%{did_you_mean_ver}/benchmark
%{gem_dir}/gems/did_you_mean-%{did_you_mean_ver}/evaluation
%{gem_dir}/gems/did_you_mean-%{did_you_mean_ver}/lib
%{gem_dir}/specifications/did_you_mean-%{did_you_mean_ver}.gemspec

%files net-telnet
%defattr(644,root,root,755)
%dir %{gem_dir}/gems/net-telnet-%{net_telnet_ver}
%{gem_dir}/gems/net-telnet-%{net_telnet_ver}/lib
%{gem_dir}/specifications/net-telnet-%{net_telnet_ver}.gemspec

%files bigdecimal
%defattr(644,root,root,755)
%{gem_dir}/gems/bigdecimal-%{bigdecimal_ver}
%dir %{gem_libdir}/bigdecimal-%{bigdecimal_ver}
%dir %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib
%attr(755,root,root) %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal.so
%{ruby_libdir}/bigdecimal
%{gem_dir}/specifications/bigdecimal-%{bigdecimal_ver}.gemspec

%files io-console
%defattr(644,root,root,755)
%{gem_dir}/gems/io-console-%{io_console_ver}
%dir %{gem_libdir}/io-console-%{io_console_ver}
%dir %{gem_libdir}/io-console-%{io_console_ver}/lib
%dir %{gem_libdir}/io-console-%{io_console_ver}/lib/io
%attr(755,root,root) %{gem_libdir}/io-console-%{io_console_ver}/lib/io/console.so
%{gem_dir}/specifications/io-console-%{io_console_ver}.gemspec

%files psych
%defattr(644,root,root,755)
%{ruby_libdir}/psych.rb
%attr(755,root,root) %{ruby_archdir}/psych.so
%{gem_dir}/gems/psych-%{psych_ver}
%{ruby_libdir}/psych
%dir %{gem_libdir}/psych-%{psych_ver}
%dir %{gem_libdir}/psych-%{psych_ver}/lib
%attr(755,root,root) %{gem_libdir}/psych-%{psych_ver}/lib/psych.so
%{gem_dir}/specifications/psych-%{psych_ver}.gemspec

%files xmlrpc
%defattr(644,root,root,755)
%{gem_dir}/gems/xmlrpc-0.2.1/Gemfile
%{gem_dir}/gems/xmlrpc-0.2.1/LICENSE.txt
%{gem_dir}/gems/xmlrpc-0.2.1/README.md
%{gem_dir}/gems/xmlrpc-0.2.1/Rakefile
%{gem_dir}/gems/xmlrpc-0.2.1/bin/console
%{gem_dir}/gems/xmlrpc-0.2.1/bin/setup
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/base64.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/client.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/config.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/create.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/datetime.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/marshal.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/parser.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/server.rb
%{gem_dir}/gems/xmlrpc-0.2.1/lib/xmlrpc/utils.rb
%{gem_dir}/specifications/xmlrpc-0.2.1.gemspec

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erb%{ruby_suffix}
%{ruby_libdir}/cgi
%{ruby_libdir}/digest
%{ruby_libdir}/drb
%{ruby_libdir}/fiddle
%{ruby_libdir}/io
%{ruby_libdir}/matrix
%{ruby_libdir}/net
%{ruby_libdir}/openssl
%{ruby_libdir}/optparse
%{ruby_libdir}/racc
%{ruby_libdir}/rbconfig
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper
%{ruby_libdir}/rss
%{ruby_libdir}/shell
%{ruby_libdir}/syslog
%{ruby_libdir}/test
%{ruby_libdir}/uri
%{ruby_libdir}/webrick
%{ruby_libdir}/yaml

%{ruby_libdir}/English.rb
%{ruby_libdir}/abbrev.rb
%{ruby_libdir}/base64.rb
%{ruby_libdir}/benchmark.rb
%{ruby_libdir}/cgi.rb
%{ruby_libdir}/cmath.rb
%{ruby_libdir}/csv.rb
%{ruby_libdir}/date.rb
%{ruby_libdir}/debug.rb
%{ruby_libdir}/delegate.rb
%{ruby_libdir}/digest.rb
%{ruby_libdir}/drb.rb
%{ruby_libdir}/e2mmap.rb
%{ruby_libdir}/erb.rb
%{ruby_libdir}/expect.rb
%{ruby_libdir}/fiddle.rb
%{ruby_libdir}/fileutils.rb
%{ruby_libdir}/find.rb
%{ruby_libdir}/forwardable.rb
%dir %{ruby_libdir}/forwardable
%{ruby_libdir}/forwardable/impl.rb
%{ruby_libdir}/getoptlong.rb
%{ruby_libdir}/ipaddr.rb
%{ruby_libdir}/json.rb
%{ruby_libdir}/kconv.rb
%{ruby_libdir}/logger.rb
%{ruby_libdir}/mathn.rb
%{ruby_libdir}/matrix.rb
%{ruby_libdir}/monitor.rb
%{ruby_libdir}/mutex_m.rb
%{ruby_libdir}/observer.rb
%{ruby_libdir}/open-uri.rb
%{ruby_libdir}/open3.rb
%{ruby_libdir}/openssl.rb
%{ruby_libdir}/optionparser.rb
%{ruby_libdir}/optparse.rb
%{ruby_libdir}/ostruct.rb
%{ruby_libdir}/pathname.rb
%{ruby_libdir}/pp.rb
%{ruby_libdir}/prettyprint.rb
%{ruby_libdir}/prime.rb
%{ruby_libdir}/profile.rb
%{ruby_libdir}/profiler.rb
%{ruby_libdir}/pstore.rb
%{ruby_libdir}/rdoc.rb
%{ruby_libdir}/resolv-replace.rb
%{ruby_libdir}/resolv.rb
%{ruby_libdir}/ripper.rb
%{ruby_libdir}/rss.rb
%{ruby_libdir}/scanf.rb
%{ruby_libdir}/securerandom.rb
%{ruby_libdir}/set.rb
%{ruby_libdir}/shell.rb
%{ruby_libdir}/shellwords.rb
%{ruby_libdir}/singleton.rb
%{ruby_libdir}/socket.rb
%{ruby_libdir}/sync.rb
%{ruby_libdir}/tempfile.rb
%{ruby_libdir}/thwait.rb
%{ruby_libdir}/time.rb
%{ruby_libdir}/timeout.rb
%{ruby_libdir}/tmpdir.rb
%{ruby_libdir}/tracer.rb
%{ruby_libdir}/tsort.rb
%{ruby_libdir}/un.rb
%{ruby_libdir}/unicode_normalize
%{ruby_libdir}/unicode_normalize.rb
%{ruby_libdir}/uri.rb
%{ruby_libdir}/weakref.rb
%{ruby_libdir}/webrick.rb
%{ruby_libdir}/yaml.rb

%if %{with batteries}
%exclude %{ruby_libdir}/rubygems.rb
%exclude %{ruby_libdir}/ubygems.rb
%exclude %{ruby_libdir}/rbconfig/datadir.rb
%endif
%exclude %{ruby_libdir}/irb.rb
%exclude %{ruby_libdir}/mkmf.rb

%{ruby_archdir}/rbconfig.rb
%attr(755,root,root) %{ruby_archdir}/bigdecimal.so
%attr(755,root,root) %{ruby_archdir}/continuation.so
%attr(755,root,root) %{ruby_archdir}/coverage.so
%attr(755,root,root) %{ruby_archdir}/date_core.so
%attr(755,root,root) %{ruby_archdir}/dbm.so
%attr(755,root,root) %{ruby_archdir}/digest.so
%attr(755,root,root) %{ruby_archdir}/etc.so
%attr(755,root,root) %{ruby_archdir}/fcntl.so
%attr(755,root,root) %{ruby_archdir}/fiber.so
%attr(755,root,root) %{ruby_archdir}/fiddle.so
%attr(755,root,root) %{ruby_archdir}/gdbm.so
%attr(755,root,root) %{ruby_archdir}/nkf.so
%attr(755,root,root) %{ruby_archdir}/objspace.so
%attr(755,root,root) %{ruby_archdir}/openssl.so
%attr(755,root,root) %{ruby_archdir}/pathname.so
%attr(755,root,root) %{ruby_archdir}/pty.so
%attr(755,root,root) %{ruby_archdir}/readline.so
%attr(755,root,root) %{ruby_archdir}/ripper.so
%attr(755,root,root) %{ruby_archdir}/sdbm.so
%attr(755,root,root) %{ruby_archdir}/socket.so
%attr(755,root,root) %{ruby_archdir}/stringio.so
%attr(755,root,root) %{ruby_archdir}/strscan.so
%attr(755,root,root) %{ruby_archdir}/syslog.so
%attr(755,root,root) %{ruby_archdir}/zlib.so

%dir %{ruby_archdir}/cgi
%attr(755,root,root) %{ruby_archdir}/cgi/escape.so
%dir %{ruby_archdir}/digest
%attr(755,root,root) %{ruby_archdir}/digest/*.so
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
%dir %{ruby_archdir}/rbconfig
%attr(755,root,root) %{ruby_archdir}/rbconfig/sizeof.so

%dir %{_libdir}/gems
%dir %{_libdir}/gems/%{oname}

%dir %{gem_dir}
%dir %{gem_dir}/gems
%dir %{gem_dir}/specifications
%dir %{gem_dir}/specifications/default
%{_mandir}/man1/erb%{ruby_suffix}.1*
%{_mandir}/man1/ri%{ruby_suffix}.1*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc ruby_%{doc_version}_stdlib
%doc ruby_%{doc_version}_core

%files doc-ri
%defattr(644,root,root,755)
%{ruby_ridir}/*
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{oname}-%{pkg_version}
