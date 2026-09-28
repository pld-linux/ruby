# Conditional build:
%bcond_without	doc		# skip (time-consuming) docs generating; intended for speed up test builds
%bcond_without	batteries	# Don't include rubygems, json, rake, minitest
%bcond_without	default_ruby	# use this Ruby as default system Ruby
%bcond_without	dtrace		# disable tracing with dtrace
%bcond_with	bootstrap	# build bootstrap version
%bcond_with	tests		# build with tests

%define		rel		1
%define		ruby_version	4.0
%define		patchlevel	7
%define		pkg_version	%{ruby_version}.%{patchlevel}
%define		ruby_suffix	%{!?with_default_ruby:%{ruby_version}}
%define		unicode_version	17.0.0
%define		oname	ruby
Summary:	Ruby - interpreted scripting language
Summary(ja.UTF-8):	オブジェクト指向言語Rubyインタプリタ
Summary(pl.UTF-8):	Ruby - interpretowany język skryptowy
Summary(pt_BR.UTF-8):	Linguagem de script orientada a objeto
Summary(zh_CN.UTF-8):	ruby - 一种快速高效的面向对象脚本编程语言
Name:		ruby
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
Source0:	https://cache.ruby-lang.org/pub/ruby/%{ruby_version}/%{oname}-%{version}.tar.xz
Source4:	rdoc.1
Source5:	testrb.1
Source6:	operating_system.rb
Patch0:		%{name}-2.3.0-ruby_version.patch
Patch1:		%{name}-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
Patch2:		%{name}-2.1.0-Enable-configuration-of-archlibdir.patch
Patch3:		strip-ccache.patch
Patch4:		%{name}-2.1.0-custom-rubygems-location.patch
# The ABRT hook used to be initialized by preludes via following patches:
# https://bugs.ruby-lang.org/issues/8566
# https://bugs.ruby-lang.org/issues/15306
# Unfortunately, due to https://bugs.ruby-lang.org/issues/16254
# and especially since https://github.com/ruby/ruby/pull/2735
# this would require boostrapping:
# https://lists.fedoraproject.org/archives/list/ruby-sig@lists.fedoraproject.org/message/LH6L6YJOYQT4Y5ZNOO4SLIPTUWZ5V45Q/
# For now, load the ABRT hook via this simple patch:
Patch6:		%{name}-2.7.0-Initialize-ABRT-hook.patch
# Disable syntax_suggest test suite, which tries to download its dependencies.
# https://bugs.ruby-lang.org/issues/19297
Patch7:		%{name}-3.3.0-Disable-syntax-suggest-test-case.patch
# Allow the rustc flags used for YJIT to be overridden.
Patch10:	%{name}-4.0.1-Support-customizable-rustc_flags-for-rustc-builds.patch
# Add ruby_version_dir_name support for RDoc (patched inside the bundled gem).
Patch11:	%{name}-2.3.0-ruby_version-Add-ruby_version_dir_name-support-for-RDoc.patch
# rdoc PR 1531: fix installation of multiple documents.
Patch12:	rdoc-pr1531-fix-mutilple-document-installation.patch
# Stop vendoring resolv for two regexps (ruby/rubygems PR 9877).
Patch13:	%{name}-4.0.7-rubygems-pr9877-stop-vendoring-resolv.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf >= 2.67
BuildRequires:	automake
BuildRequires:	bison >= 1.875
BuildRequires:	coreutils
BuildRequires:	db-devel
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	gmp-devel
BuildRequires:	libffi-devel
BuildRequires:	libstdc++-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel >= 0.9.6
BuildRequires:	pkgconfig
BuildRequires:	readline-devel >= 4.2
BuildRequires:	rpm-build >= 5.4.10-49
BuildRequires:	rpmbuild(macros) >= 1.527
# which version is minimum now? 1.8.7 is not enough, fails with:
# ./tool/generic_erb.rb:31: syntax error, unexpected ':', expecting ')'
# ...O.popen("tput smso", "r", err: IO::NULL, &:read) rescue nil)
BuildRequires:	ruby >= 1:1.9
BuildRequires:	rust
BuildRequires:	sed >= 4.0
%{?with_dtrace:BuildRequires:	systemtap-sdt-devel}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yaml-devel
BuildRequires:	zlib-devel
%if %{without bootstrap}
# bootstrap needs ruby binary, erb module
BuildRequires:	rpm-rubyprov
BuildRequires:	ruby-modules
%endif
Requires(post,postun):	/sbin/ldconfig
Provides:	ruby(release) = %{ruby_version}
Obsoletes:	ruby-REXML <= 2.4.0-2
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread <= 0.6.3
Conflicts:	rpm-build-macros < 1.695
Conflicts:	ruby-activesupport < 2.3.11-2
Conflicts:	ruby-activesupport2 < 2.3.11-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# relative symlinks
# usage: %make_rel_symlink <target-in-install-root> [<directory> [<link-name>]]
# e.g.  %%make_rel_symlink %%{gem_instdir rdoc}/lib/rdoc %%{ruby_libdir}
# creates <directory>/<link-name> as a symlink holding the shortest relative
# path to <target>, so that it stays valid after installation.  <link-name>
# defaults to the basename of <target>.
%define rel_symlink()  %(realpath -m --relative-to=%{buildroot}%{?2} %{buildroot}%{?1})
%define make_rel_symlink()  ln -s %{rel_symlink %{?1} %{?2}} %{buildroot}%{?2}/%{?3}%{!?3:%(basename %{?1})}

# hack: skip rubygem(ipaddr)
%define	_noautoreq	ipaddr
# ruby(abi) replaced by ruby(release)
%{expand:%%global _noautoreq %{_noautoreq} 'ruby\\(abi\\)'}
%{expand:%%global _noautoprov %{?nil} 'ruby\\(abi\\)'}

# Bundled libraries versions
%define rubygems_version 4.0.20

# Default gems.
%define bundler_version 4.0.20
%define erb_version 6.0.7


%define io_console_version 0.8.2
%define irb_version 1.16.0
%define json_version 2.18.0
%define psych_version 5.3.1
%define rdoc_version 7.0.4
%define syntax_suggest_version 2.0.3

%define benchmark_version 0.5.0
%define fiddle_version 1.1.8
%define logger_version 1.7.0
%define ostruct_version 0.6.3
%define pstore_version 0.2.1
%define readline_version 0.0.4
%define reline_version 0.6.3
# Bundled gems.
%define abbrev_version 0.1.2
%define base64_version 0.3.0
%define bigdecimal_version 4.0.1
%define csv_version 3.3.5
%define debug_version 1.11.1
%define drb_version 2.2.3
%define getoptlong_version 0.2.1
%define matrix_version 0.4.3
%define minitest_version 6.0.0
%define mutex_m_version 0.3.0
%define net_ftp_version 0.3.9
%define net_imap_version 0.6.4.1
%define net_pop_version 0.1.2
%define net_smtp_version 0.5.1
%define nkf_version 0.2.0
%define observer_version 0.1.2
%define power_assert_version 3.0.1
%define prime_version 0.1.4
%define racc_version 1.8.1
%define rake_version 13.3.1
%define rbs_version 3.10.0
%define repl_type_completor_version 0.1.12
%define resolv_replace_version 0.1.1
%define rexml_version 3.4.4
%define rinda_version 0.2.0
%define rss_version 0.3.2
%define syslog_version 0.3.0
%define test_unit_version 3.7.5
%define typeprof_version 0.31.1

# Bundled nkf version
%global bundled_nkf_version 2.1.5

%define	ruby_ridir		%{_datadir}/ri/system
%define	gem_dir			%{_datadir}/gems
%define	gem_archdir		%{_libdir}/gems/%{oname}

# Fedora macros
%define gem_version()   %{?1:%{expand:%{%{gsub %{1} - _}_version}}}%{!?1:%{version}}
%define gem_name_version()   %{?1}%{!?1:%{gem_name}}-%{gem_version %{?1}}
%define gem_instdir()   %{gem_dir}/gems/%{gem_name_version %{?1}}
%define gem_libdir()   %{gem_instdir %{?1}}/lib
%define gem_extdir_mri()   %{gem_archdir}/%{gem_name_version %{?1}}
%define gem_spec(d)   %{gem_dir}/specifications%{?-d:/default}/%{gem_name_version %{?1}}.gemspec
%define gem_cache()   %{gem_dir}/cache/%{gem_name_version %{?1}}.gem
%define gem_docdir()   %{gem_dir}/doc/%{gem_name_version %{?1}}
%define gem_plugin()   %{gem_dir}/plugins/%{?1}%{!?1:%{gem_name}}_plugin.rb

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
Provides:	ruby(release) = %{ruby_version}
%requires_ge_to openssl openssl-devel

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
Obsoletes:	ruby-static < 1:2.4

%description devel
Ruby development libraries.

%description devel -l pl.UTF-8
Biblioteki programistyczne interpretera języka Ruby.

%package doc-ri
Summary:	Ruby ri documentation
Summary(pl.UTF-8):	Dokumentacja Ruby w formacie ri
Group:		Documentation
Requires:	%{name}-modules = %{epoch}:%{version}-%{release}
BuildArch:	noarch

%description doc-ri
Ruby ri documentation.

%description doc-ri -l pl.UTF-8
Dokumentacja Ruby w formacie ri.

%package examples
Summary:	Ruby examples
Summary(pl.UTF-8):	Przykłady dla języka Ruby
Group:		Development/Languages
Requires:	ruby(release) = %{ruby_version}
BuildArch:	noarch

%description examples
Ruby examples.

%description examples -l pl.UTF-8
Przykłady programów w języku Ruby.

# IMPORTANT: keep irb, rdoc, rubygems, rake, json as last packages as we reset epoch/version/release
# and version, release macros may not be used directly as they take last
# subpackage value not main package one what you intend to use

%package irb
Summary:	The Interactive Ruby
Summary(pl.UTF-8):	Interaktywny Ruby
Version:	%{irb_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Languages
Requires:	%{name}-modules = 1:%{pkg_version}-%{rel}
Provides:	irb = %{version}-%{release}
Provides:	ruby(irb) = %{version}-%{release}
BuildArch:	noarch

%description irb
The irb is acronym for Interactive Ruby. It evaluates ruby expression
from the terminal.

%description irb -l pl.UTF-8
Nazwa irb to skrót od Interactive Ruby (interaktywny Ruby). Wyznacza
wartości wyrażeń języka ruby podane z terminala.

%package rdoc
Summary:	A tool to generate HTML and command-line documentation for Ruby projects
Summary(pl.UTF-8):	Narzędzie do generowania dokumentacji HTML i linii poleceń dla projektów w Rubym
Version:	%{rdoc_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
# SIL: lib/rdoc/generator/template/darkfish/css/fonts.css
License:	GPLv2 and Ruby and MIT and SIL
Group:		Development/Libraries
Requires:	%{name}-irb >= %{irb_version}
Requires:	%{name}-json >= %{json_version}
Requires:	%{name}-modules = 1:%{pkg_version}-%{rel}
Obsoletes:	rdoc <= 0.9.0
BuildArch:	noarch

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
Version:	%{rubygems_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	Ruby or MIT
Group:		Development/Libraries
Requires:	%{name}-bigdecimal = %{bigdecimal_version}-%{pkg_version}.%{rel}
Requires:	%{name}-io-console = %{io_console_version}-%{pkg_version}.%{rel}
Requires:	%{name}-modules = 1:%{pkg_version}-%{rel}
Requires:	%{name}-psych = %{psych_version}-%{pkg_version}.%{rel}
Requires:	%{name}-rdoc >= %{rdoc_version}
Suggests:	%{name}-devel
Provides:	rubygems = %{rubygems_version}
BuildArch:	noarch

%description rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%description rubygems -l pl.UTF-8
RubyGems to standardowe narzędzie języka Ruby do publikowania i
zarządzania zewnętrznymi bibliotekami.

%package bundler
Summary:	Library and utilities to manage a Ruby application's gem dependencies
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Biblioteka i narzędzia do zarządzania zależnościami gem aplikacji w języku Ruby
Version:	%{bundler_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Languages
Provides:	bundler = %{bundler_version}
BuildArch:	noarch

%description bundler
Bundler manages an application's dependencies through its entire life,
across many machines, systematically and repeatably.

%description bundler -l pl.UTF-8
Bundler zarządza zależnościami aplikacji przez cały czas jej życia,
między wiloma maszynami - systematycznie i powtarzalnie.

%package rake
Summary:	Rake is a Make-like program implemented in Ruby
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Program typu Make dla języka Ruby
Version:	%{rake_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Languages
Provides:	rake = %{rake_version}
Conflicts:	ruby-modules < 1:1.9.3.429-2
BuildArch:	noarch

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
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Biblioteka JSON dla języka Ruby
Version:	%{json_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
# UCD: ext/json/generator/generator.c
License:	(Ruby or GPL v2) and UCD
Group:		Development/Languages
Obsoletes:	ruby-json-rubyforge < 1
Conflicts:	ruby-modules < 1:1.9.3.429-3

%description json
This is a JSON implementation as a Ruby extension in C.

%description json -l pl.UTF-8
Biblioteka JSON dla języka Ruby.

%package minitest
Summary:	Minitest - a complete suite of testing facilities
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Minitest - kompletny szkielet do testowania
Version:	%{minitest_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries
BuildArch:	noarch

%description minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.

%description minitest -l pl.UTF-8
minitest/unit to mały i bardzo szybki szkielet testów jednostkowych.

minitest/spec to funkcjonalnie kompletny silnik specyfikacji.

minitest/benchmark to wspaniały sposób zapewnienia wydajności
algorytmów w powtarzalny sposób.

minitest/mock autorstwa Stevena Bakera to mały szkielet obiektów
atrap.

minitest/pride ukazuje dumę z testowania i dodaje kolorowanie do
wyjścia testów.

%package power_assert
Summary:	Power Assert for Ruby
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Power Assert dla języka Ruby
Version:	%{power_assert_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	Ruby or BSD
Group:		Development/Libraries
BuildArch:	noarch

%description power_assert
Power Assert shows each value of variables and method calls in the
expression. It is useful for testing, providing which value wasn't
correct when the condition is not satisfied.

%description power_assert -l pl.UTF-8
Power Assert pokazuje każdą wartość zmiennych i wywołań metod w
wyrażeniu. Jest przydatny do testowania, ukazując, która wartość nie
była poprawna, kiedy warunek nie był spełniony.

%package test-unit
Summary:	An xUnit family unit testing framework for Ruby
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Szkielet testów z rodziny xUnit dla języka Ruby
Version:	%{test_unit_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:	(Ruby or BSD) and (Ruby or BSD or Python) and (Ruby or BSD or LGPL v2+)
Group:		Development/Libraries
Requires:	ruby-power_assert = %{power_assert_version}-%{pkg_version}.%{rel}
BuildArch:	noarch

%description test-unit
test-unit (Test::Unit) is unit testing framework for Ruby, based on
xUnit principles. These were originally designed by Kent Beck, creator
of extreme programming software development methodology, for
Smalltalk's SUnit. It allows writing tests, checking results and
automated testing in Ruby.

%description test-unit -l pl.UTF-8
test-unit (Test::Unit) to szkielet testów jednostkowych dla języka
Ruby oparty na zasadach xUnit. Te były pierwotnie zaprojektowane przez
Kenta Becka, twórcy metodyki tworzenia oprogramowania zwanej
programowaniem ekstremalnym, dla szkieletu SUnit dla Smalltalka.
Szkielet pozwala na pisanie testów, sprawdzanie wyników i automatyczne
testowanie w Rubym.

%package racc
Summary:	Racc is a LALR(1) parser generator
Version:	%{racc_version}
License:	Ruby OR BSD-2-Clause
URL:		https://github.com/ruby/racc
Requires:	ruby(release) = %{ruby_version}

%description racc
Racc is a LALR(1) parser generator. It is written in Ruby itself, and
generates Ruby program.

%package rbs
Summary:	Type signature for Ruby
Version:	%{rbs_version}
Release:	%{pkg_version}.%{rel}
License:	MIT
Group:		Development/Libraries
Requires:	ruby(release) = %{ruby_version}

%description rbs
RBS is the language for type signatures for Ruby and standard library
definitions.

%package typeprof
Summary:	TypeProf is a type analysis tool for Ruby code based on abstract interpretation
Version:	%{typeprof_version}
Release:	%{pkg_version}.%{rel}
License:	MIT
URL:		https://github.com/ruby/typeprof
Requires:	ruby(release) = %{ruby_version}
BuildArch:	noarch

%description typeprof
TypeProf performs a type analysis of non-annotated Ruby code. It
abstractly executes input Ruby code in a level of types instead of
values, gathers what types are passed to and returned by methods, and
prints the analysis result in RBS format, a standard type description
format for Ruby 3.x

%package bigdecimal
Summary:	BigDecimal - arbitrary-precision floating point decimal arithmetic
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	BigDecimal - dziesiętna arytmetyka zmiennoprzecinkowa o dowolnej dokładności
Version:	%{bigdecimal_version}
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
calculation, because it provides the correct answers people expect -
whereas normal binary floating point arithmetic often introduces
subtle errors because of the conversion between base 10 and base 2.

%description bigdecimal -l pl.UTF-8
Ruby zapewnia wbudowaną obsługę arytmetyki całkowitej dowolnej
dokładności, np.:

42**13 -> 1265437718438866624512

BigDecimal zapewnia podobną obsługę bardzo dużych lub bardzo
dokładnych liczb zmiennoprzecinkowych. Arytmetyka dziesiętna jest
przydatna także do ogólnych obliczeń, ponieważ zapewnia poprawne
odpowiedzi oczekiwane przez ludzi - podczas gdy normalna binarna
arytmetyka zmiennoprzecinkowa wprowadza minimalne błędy spowodowane
zmianą podstawy między 10 a 2.

%package io-console
Summary:	IO/Console - a simple console utilizing library
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	IO/Console - prosta biblioteka wykorzystująca konsolę
Version:	%{io_console_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Libraries

%description io-console
IO/Console provides very simple and portable access to console. It
doesn't provide higher layer features, such like curses and readline.

%description io-console -l pl.UTF-8
IO/Console zapewnia bardzo prosty i przenośny dostęp do konsoli. Nie
udostępnia funkcji wyższego poziomu, takich jak curses czy readline.

%package psych
Summary:	A libyaml wrapper for Ruby
Requires:	ruby(release) = %{ruby_version}
Summary(pl.UTF-8):	Obudowanie libyaml dla języka Ruby
Version:	%{psych_version}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries

%description psych
Psych is a YAML parser and emitter. Psych leverages libyaml for its
YAML parsing and emitting capabilities. In addition to wrapping
libyaml, Psych also knows how to serialize and de-serialize most Ruby
objects to and from the YAML format.

%description psych -l pl.UTF-8
Psych to parser i emiter YAML. Wykorzystuje libyaml do analizy i
emitowania YAML-a. Poza obudowaniem libyaml, wie także jak
serializować i deserializować większość obiektów języka Ruby do/z
formatu YAML.

%package rexml
Summary:	An XML toolkit for Ruby
Version:	%{rexml_version}
Release:	%{pkg_version}.%{rel}
License:	BSD
URL:		https://github.com/ruby/rexml
Requires:	ruby(release) = %{ruby_version}
BuildArch:	noarch

%description rexml
REXML was inspired by the Electric XML library for Java, which
features an easy-to-use API, small size, and speed. Hopefully, REXML,
designed with the same philosophy, has these same features. I've tried
to keep the API as intuitive as possible, and have followed the Ruby
methodology for method naming and code flow, rather than mirroring the
Java API.

REXML supports both tree and stream document parsing. Stream parsing
is faster (about 1.5 times as fast). However, with stream parsing, you
don't get access to features such as XPath.

%package rss
Summary:	Family of libraries that support various formats of XML "feeds"
Version:	%{rss_version}
License:	BSD
URL:		https://github.com/ruby/rss
Requires:	ruby(release) = %{ruby_version}
BuildArch:	noarch

%description rss
Really Simple Syndication (RSS) is a family of formats that describe
'feeds', specially constructed XML documents that allow an interested
person to subscribe and receive updates from a particular web service.
This library provides tooling to read and create these feeds.

%package bundled-gems
Summary:	Bundled gems which are part of Ruby StdLib
Requires:	ruby-rubygems >= %{rubygems_version}
# Runtime dependency of rubygem(debug).
Recommends:	rubygem(irb) >= %{irb_version}
Requires:	ruby(release) = %{ruby_version}
Provides:	rubygem(abbrev) = %{abbrev_version}
Provides:	rubygem(base64) = %{base64_version}
Provides:	rubygem(csv) = %{csv_version}
Provides:	rubygem(debug) = %{debug_version}
Provides:	rubygem(drb) = %{drb_version}
Provides:	rubygem(getoptlong) = %{getoptlong_version}
Provides:	rubygem(matrix) = %{matrix_version}
Provides:	rubygem(mutex_m) = %{mutex_m_version}
Provides:	rubygem(net-ftp) = %{net_ftp_version}
Provides:	rubygem(net-imap) = %{net_imap_version}
Provides:	rubygem(net-pop) = %{net_pop_version}
Provides:	rubygem(net-smtp) = %{net_smtp_version}
Provides:	rubygem(nkf) = %{bundled_nkf_version}
Provides:	rubygem(nkf) = %{nkf_version}
Provides:	rubygem(observer) = %{observer_version}
Provides:	rubygem(prime) = %{prime_version}
Provides:	rubygem(repl_type_completor) = %{repl_type_completor_version}
Provides:	rubygem(resolv-replace) = %{resolv_replace_version}
Provides:	rubygem(rinda) = %{rinda_version}
Provides:	rubygem(syslog) = %{syslog_version}

%description bundled-gems
Bundled gems which are part of Ruby StdLib. While being part of Ruby,
these needs to be listed in Gemfile to be used by Bundler.

%prep
%setup -q -n %{oname}-%{pkg_version}
%patch 0 -p1
%patch 1 -p1
%patch 2 -p1
%patch 3 -p1
%patch 4 -p1
%patch 6 -p1
%patch 7 -p1
%patch 10 -p1
%patch 13 -p1

# The bundled rdoc is a gem, so it has to be patched in place.
cd .bundle/gems/rdoc-%{rdoc_version}
%patch 11 -p1
%patch 12 -p1
cd %{builddir}/%{buildsubdir}

# must be regenerated with new bison
%{__rm} parse.{c,h}

# Remove bundled libraries to be sure they are not used.
#%{__rm} -r ext/psych/yaml
#%{__rm} -r ext/fiddle/libffi*

# Install custom operating_system.rb.
#
# "make install" runs "require 'rubygems/defaults/operating_system'".  Without
# this file that require falls through to /usr/share/ruby/%{ruby_version} and
# happily picks up the copy from an already installed RubyGems, which then
# points Gem.default_dir at the per-user gem directory.  Since -I../lib comes
# first on the load path, the copy in the tree always wins.
install -d lib/rubygems/defaults
cp -p %{SOURCE6} lib/rubygems/defaults

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

find -type f '(' -name '*.rb' -o -name '*.cgi' -o -name '*.test' \
	-o -name 'ruby.1' -o -name '*.html' -o -name '*.tcl' ')' \
| xargs %{__sed} -i 's,%{_prefix}/local/bin/,%{_bindir}/,'

%if %{with bootstrap}
# avoid regeneration, needs iostring module
touch enc/unicode/%{unicode_version}/*.h
%endif

%build
rubygems_version=$(awk '/VERSION =/ && $1 == "VERSION" {print $3}' lib/rubygems.rb | sed 's/\.freeze//g' | xargs)
if [ $rubygems_version != %{rubygems_version} ]; then
	echo "Set %%define rubygems_version to $rubygems_version and re-run."
	exit 1
fi
rdoc_version=$(awk '/VERSION =/ && $1 == "VERSION" {print $3}' .bundle/gems/rdoc-%{rdoc_version}/lib/rdoc/version.rb | xargs)
if [ "$rdoc_version" != %{rdoc_version} ]; then
	echo "Set %%define rdoc_version to $rdoc_version and re-run."
	exit 1
fi

cp -f /usr/share/automake/config.sub .

%{__autoconf}

# The %%configure macro runs %%_configure (default: ./configure) in the current
# directory. For a VPATH build we are in build/, but the real configure script
# lives in the source directory, hence the wrapper created below.
mkdir -p %{_vpath_builddir}
cd %{_vpath_builddir}
rm -f configure
ln -sf ../tool
cp -f /usr/share/automake/install-sh tool/
cat > configure <<'EOF'
#!/bin/sh
exec ../configure "$@"
EOF
chmod +x configure

%configure \
	%{?with_bootstrap:--with-baseruby="%{_bindir}/ruby -I$(pwd)/lib"} \
	--with-rubylibprefix='%{ruby_libdir}' \
	--with-archlibdir='%{_libdir}' \
	--with-rubyarchprefix='%{ruby_libarchdir}' \
	--with-sitedir='%{ruby_sitelibdir}' \
	--with-sitearchdir='%{ruby_sitearchdir}' \
	--with-vendordir='%{ruby_vendorlibdir}' \
	--with-vendorarchdir='%{ruby_vendorarchdir}' \
	--with-rubyhdrdir='%{_includedir}' \
	--with-rubyarchhdrdir='%{_includedir}' \
	--with-sitearchhdrdir='$(sitehdrdir)/$(arch)' \
	--with-vendorarchhdrdir='$(vendorhdrdir)/$(arch)' \
	--with-rubygemsdir='%{rubygems_dir}' \
	--with-ruby-pc='ruby.pc' \
	--with-compress-debug-sections=no \
	--disable-rpath \
	--enable-mkmf-verbose \
	--enable-shared \
	--with-ruby-version='' \
	--enable-multiarch \
%ifarch %{x8664} aarch64
	--enable-yjit \
%endif
	--disable-install-doc \

cd ..

%make_build COPY="cp -p" -C %{_vpath_builddir}

%if %{with doc}
%{__make} -C %{_vpath_builddir} -j1 rdoc
%endif

%install

rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rdocdir},%{ruby_ridir}} \
	$RPM_BUILD_ROOT%{ruby_vendorarchdir} \
	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/net \
	$RPM_BUILD_ROOT%{ruby_vendorlibdir}/data



%make_install -C %{_vpath_builddir}
%if %{with doc}
%{__make} -C %{_vpath_builddir} install-doc DESTDIR=%{buildroot}
%endif

# `ruby` executable is placed in some strange directory
# https://bugs.ruby-lang.org/issues/20800
# https://github.com/ruby/ruby/pull/12043
CONFIG_TARGET_DIR=%{buildroot}%{_exec_prefix}/$( \
  %{_vpath_builddir}/miniruby -I%{_vpath_builddir} -rrbconfig -e 'puts RbConfig::CONFIG["config_target"]' \
)
mv ${CONFIG_TARGET_DIR}/bin/ruby %{buildroot}%{_bindir}
rm -rd ${CONFIG_TARGET_DIR}

# Version is empty if --with-ruby-version is specified.
# http://bugs.ruby-lang.org/issues/7807
sed -i 's/Version: \${ruby_version}/Version: %{ruby_version}/' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

# Kill bundled certificates, as they should be part of ca-certificates.
# Newer RubyGems releases no longer ship them, hence the -f.
for cert in GlobalSignRootCA.pem GlobalSignRootCA_R3.pem; do \
    %{__rm} -f $RPM_BUILD_ROOT%{rubygems_dir}/rubygems/ssl_certs/*/$cert
done
# Ensure there is not forgotten any certificate.
##test ! "$(ls -A $RPM_BUILD_ROOT%{rubygems_dir}/rubygems/ssl_certs/ 2>/dev/null)"

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}
cp -Rf sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}

# "make install" no longer installs the top level documentation.
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-%{pkg_version}
cp -p NEWS.md LEGAL BSDL README.md README.EXT $RPM_BUILD_ROOT%{_docdir}/%{name}-%{pkg_version}/
cp -p %{SOURCE4} %{buildroot}%{_mandir}/man1/rdoc.1
cp -p %{SOURCE5} %{buildroot}%{_mandir}/man1/testrb.1

%{__rm} -rf $RPM_BUILD_ROOT%{_docdir}/%{name}/html

# Move gems root into common directory, out of Ruby directory structure.
# "make install" already lays it out as %{gem_dir}/{gems,specifications,extensions}.
# The bundled gem cache is not packaged.
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/gems $RPM_BUILD_ROOT%{gem_dir}
%{__rm} -f $RPM_BUILD_ROOT%{gem_dir}/cache/*.gem

# Install the packager overrides for RubyGems.  This has to happen after the
# gems have been moved, so that Gem.default_dirs[:system] points at %{gem_dir}.
install -d $RPM_BUILD_ROOT%{rubygems_dir}/rubygems/defaults
cp -p %{SOURCE6} $RPM_BUILD_ROOT%{rubygems_dir}/rubygems/defaults

# Move bundled rubygems to %gem_dir
# make symlinks for io-console and bigdecimal, which are considered to be part of stdlib by other Gems
# make symlinks for all packages, so they would work without rubygems
# NOTE: when making symlinks, do not symlink paths that could be directories,
# as there may came files from other packages as well. actually, unlikely as
# the links to got system dir and only ruby may package there (other distro
# packages should go to vendor dirs)%
# Since Ruby 4.0 "make install" already places the bundled gems below
# %{gem_dir}, so nothing has to be moved out of %{ruby_libdir} here.
[ -d $RPM_BUILD_ROOT%{gem_spec -d rdoc} ] && \
    %{__mv} $RPM_BUILD_ROOT%{gem_spec -d rdoc} $RPM_BUILD_ROOT%{gem_dir}/specifications
%make_rel_symlink %{gem_instdir rdoc}/lib/rdoc %{ruby_libdir}
%make_rel_symlink %{gem_instdir rdoc}/lib/rdoc.rb %{ruby_libdir}

%make_rel_symlink %{gem_instdir bigdecimal}/lib/bigdecimal %{ruby_libdir}
%make_rel_symlink %{gem_instdir bigdecimal}/lib/bigdecimal.rb %{ruby_libdir}
%make_rel_symlink %{gem_extdir_mri bigdecimal}/bigdecimal.so %{ruby_libarchdir}

install -d $RPM_BUILD_ROOT%{gem_instdir io-console}/lib
install -d $RPM_BUILD_ROOT%{gem_extdir_mri io-console}/lib/io
touch $RPM_BUILD_ROOT%{gem_extdir_mri io-console}/gem.build_complete
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/io $RPM_BUILD_ROOT%{gem_instdir io-console}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/io/console.so $RPM_BUILD_ROOT%{gem_extdir_mri io-console}/lib/io
%{__mv} $RPM_BUILD_ROOT%{gem_spec -d io-console} $RPM_BUILD_ROOT%{gem_dir}/specifications
%make_rel_symlink %{gem_instdir io-console}/lib/io %{ruby_libdir}
%make_rel_symlink %{gem_extdir_mri io-console}/lib/io/console.so %{ruby_libarchdir}/io

install -d $RPM_BUILD_ROOT%{gem_instdir json}/lib
install -d $RPM_BUILD_ROOT%{gem_extdir_mri json}/lib
touch $RPM_BUILD_ROOT%{gem_extdir_mri json}/gem.build_complete
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/json* $RPM_BUILD_ROOT%{gem_instdir json}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/json $RPM_BUILD_ROOT%{gem_extdir_mri json}/lib
%{__mv} $RPM_BUILD_ROOT%{gem_spec -d json} $RPM_BUILD_ROOT%{gem_dir}/specifications
%make_rel_symlink %{gem_instdir json}/lib/json %{ruby_libdir}
%make_rel_symlink %{gem_instdir json}/lib/json.rb %{ruby_libdir}
install -d $RPM_BUILD_ROOT%{ruby_libarchdir}/json/ext
%make_rel_symlink %{gem_extdir_mri json}/lib/json/ext/parser.so %{ruby_libarchdir}/json/ext
%make_rel_symlink %{gem_extdir_mri json}/lib/json/ext/generator.so %{ruby_libarchdir}/json/ext

%make_rel_symlink %{gem_instdir minitest}/lib/minitest %{ruby_libdir}

install -d $RPM_BUILD_ROOT%{ruby_libdir}/test
%make_rel_symlink %{gem_instdir test-unit}/lib/test/unit %{ruby_libdir} test/unit

install -d $RPM_BUILD_ROOT%{gem_instdir psych}/lib
install -d $RPM_BUILD_ROOT%{gem_extdir_mri psych}/lib
touch $RPM_BUILD_ROOT%{gem_extdir_mri psych}/gem.build_complete
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/psych* $RPM_BUILD_ROOT%{gem_instdir psych}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/psych.so $RPM_BUILD_ROOT%{gem_extdir_mri psych}/lib/
%{__mv} $RPM_BUILD_ROOT%{gem_spec -d psych} $RPM_BUILD_ROOT%{gem_dir}/specifications
%make_rel_symlink %{gem_instdir psych}/lib/psych %{ruby_libdir}
%make_rel_symlink %{gem_instdir psych}/lib/psych.rb %{ruby_libdir}
%make_rel_symlink %{gem_extdir_mri psych}/lib/psych.so %{ruby_archdir}

#install -d $RPM_BUILD_ROOT%{gem_libdir bundler}
#%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/bundler.rb $RPM_BUILD_ROOT%{gem_libdir bundler}
#%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/bundler $RPM_BUILD_ROOT%{gem_libdir bundler}
#%{__mv} $RPM_BUILD_ROOT%{gem_spec -d bundler} $RPM_BUILD_ROOT%{gem_spec bundler}

install -d $RPM_BUILD_ROOT%{gem_instdir bundler}/lib
install -d $RPM_BUILD_ROOT%{gem_extdir_mri bundler}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/bundler* $RPM_BUILD_ROOT%{gem_instdir bundler}/lib
%{__mv} $RPM_BUILD_ROOT%{gem_spec -d bundler} $RPM_BUILD_ROOT%{gem_dir}/specifications
%make_rel_symlink %{gem_instdir bundler}/lib/bundler %{ruby_libdir}
%make_rel_symlink %{gem_instdir bundler}/lib/bundler.rb %{ruby_libdir}

# Move the binary extensions into proper place (if no gem has binary extension,
# the extensions directory might be empty).
for extdir in "$RPM_BUILD_ROOT"%{gem_dir}/extensions \
              "$RPM_BUILD_ROOT"/../%{oname}-%{pkg_version}/build/.bundle/extensions; do
    [ -d "$extdir" ] || continue
    find "$extdir"/*-%{_target_os}/%{ruby_version}.*/* -maxdepth 0 \
        -exec mv '{}' $RPM_BUILD_ROOT%{_libdir}/gems/%{name}/ \; \
        || echo "No gem binary extensions to move."
done
# Only the leftovers in the build root; the source tree must stay intact for
# the "gem build_complete" stamps and for subsequent extension builds.
rm -rf "$RPM_BUILD_ROOT"%{gem_dir}/extensions

# Remove the extension sources and library copies from `lib` dir.
find $RPM_BUILD_ROOT%{gem_dir}/gems/*/ext -maxdepth 0 -exec rm -rf '{}' +
find $RPM_BUILD_ROOT%{gem_dir}/gems/*/lib -name \*.so -delete

# replace default irb with its not gemified version
%{__mv} $RPM_BUILD_ROOT%{gem_instdir irb}/exe/irb %{buildroot}%{_bindir}/irb
# syntax_suggest is installed without suffix by default

# Adjust the gemspec files so that the gems will load properly
sed -i '/^end$/ i\
  s.require_paths = ["lib"]' $RPM_BUILD_ROOT%{gem_spec rake}

sed -i '/^end$/ i\
  s.require_paths = ["lib"]' $RPM_BUILD_ROOT%{gem_spec rdoc}

sed -i '/^end$/ i\
  s.require_paths = ["lib"]\
  s.extensions = ["bigdecimal.so"]' $RPM_BUILD_ROOT%{gem_spec bigdecimal}

sed -i '/^end$/ i\
  s.require_paths = ["lib"]\
  s.extensions = ["io/console.so"]' $RPM_BUILD_ROOT%{gem_spec io-console}

sed -i '/^end$/ i\
  s.require_paths = ["lib"]\
  s.extensions = ["json/ext/parser.so", "json/ext/generator.so"]' $RPM_BUILD_ROOT%{gem_spec json}

sed -i '/^end$/ i\
  s.require_paths = ["lib"]' $RPM_BUILD_ROOT%{gem_spec minitest}

# Push the .gemspecs through the RubyGems to let them write the stub headers.
# This speeds up loading of libraries and avoids warnings in Spring:
# https://github.com/rubygems/rubygems/pull/694
for s in rake-%{rake_version}.gemspec rdoc-%{rdoc_version}.gemspec json-%{json_version}.gemspec; do
	s="$RPM_BUILD_ROOT%{gem_dir}/specifications/$s"
	%{__make} -C %{_vpath_builddir} runruby TESTRUN_SCRIPT="-rrubygems \
	-e \"spec = Gem::Specification.load('$s')\" \
	-e \"File.write '$s', spec.to_ruby\""
done

# Rewrite gem shebangs.  Newer gems may use the "#!/usr/bin/env -S ruby"
# form, which rpm's shebang check rejects.
%{__sed} -i -e '1s,/usr/bin/env -S ruby,%{_bindir}/ruby,' \
        -e '1s,/usr/bin/env ruby,%{_bindir}/ruby,' \
        $(find $RPM_BUILD_ROOT -type f | xargs grep -l -E '%{_bindir}/env (-S )?ruby' 2>/dev/null)

# gem non library files
rm -rf $RPM_BUILD_ROOT%{gem_instdir debug}/{[A-Z]*,misc,exts.mk}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir matrix}/[A-Z]*
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir minitest}/{[A-Z]*,test}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir net-ftp}/[A-Z]*
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir net-pop}/[A-Z]*
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir net-imap}/{[A-Z]*,docs}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir net-smtp}/[A-Z]*
rm -f $RPM_BUILD_ROOT%{gem_instdir nkf}/exts.mk 2>/dev/null || :
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir power_assert}/[A-Z]*
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir prime}/[A-Z]*
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir racc}/{[A-Z]*,doc}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir rake}/{[A-Z]*,doc}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir test-unit}/{[A-Z]*,doc,sample}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir rexml}/{[A-Z]*,doc}
%{__rm} -r $RPM_BUILD_ROOT%{gem_instdir rss}/[A-Z]*
rm -rf $RPM_BUILD_ROOT%{gem_instdir syslog}/{[A-Z]*,exts.mk}

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
rm -f $RPM_BUILD_ROOT%{ruby_ridir}/cache.ri 2>/dev/null || :
%endif

%check
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

%{__make} -C %{_vpath_builddir} check TESTS="-v $DISABLE_TESTS"
%endif

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc %{_docdir}/%{name}-%{pkg_version}/NEWS.md
%doc %{_docdir}/%{name}-%{pkg_version}/LEGAL
%doc %{_docdir}/%{name}-%{pkg_version}/BSDL
%doc %{_docdir}/%{name}-%{pkg_version}/README.md
%doc %{_docdir}/%{name}-%{pkg_version}/README.EXT
%attr(755,root,root) %{_bindir}/ruby
%{_libdir}/libruby.so.*.*.*
%ghost %{_libdir}/libruby.so.%{ruby_version}
%{_mandir}/man1/ruby.1*

%dir %{_libdir}/%{oname}
%dir %{_libdir}/%{oname}/%{vendordir}
%dir %{_datadir}/%{oname}

%dir %{ruby_libdir}
%dir %{ruby_archdir}
%dir %{ruby_vendorlibdir}
%dir %{ruby_vendorarchdir}

# Since RDoc 7 the ri data is versioned below %%{_datadir}/ri/%%{ruby_version} and
# is packaged by ruby-doc-ri, so the old unversioned %%{ruby_ridir} is gone.
%dir %{ruby_rdocdir}

# common dirs for ruby vendor modules
%dir %{ruby_vendorlibdir}/data
%dir %{ruby_vendorlibdir}/net

%files devel
%defattr(644,root,root,755)
%{_libdir}/libruby.so
%{_includedir}/*
%{_pkgconfigdir}/ruby.pc
%{ruby_libdir}/mkmf.rb

%files irb
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/irb
%{gem_instdir irb}
%{gem_spec irb}

%files rdoc
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rdoc
%attr(755,root,root) %{_bindir}/ri
%{_mandir}/man1/rdoc.1*
%{gem_instdir rdoc}/man/ri.1*
%{ruby_libdir}/rdoc
%dir %{gem_instdir rdoc}
%{gem_instdir rdoc}/lib
%{gem_spec rdoc}
%{gem_instdir rdoc}/rdoc.gemspec
%dir %{gem_instdir rdoc}/exe
%{gem_instdir rdoc}/exe/rdoc
%{gem_instdir rdoc}/exe/ri
%{gem_plugin rdoc}
%doc %{gem_instdir rdoc}/CONTRIBUTING.md
%doc %{gem_instdir rdoc}/CVE-2013-0256.rdoc
%doc %{gem_instdir rdoc}/ExampleMarkdown.md
%doc %{gem_instdir rdoc}/ExampleRDoc.rdoc
%doc %{gem_instdir rdoc}/History.rdoc
%license %{gem_instdir rdoc}/LEGAL.rdoc
%license %{gem_instdir rdoc}/LICENSE.rdoc
%doc %{gem_instdir rdoc}/README.md
%doc %{gem_instdir rdoc}/RI.md
%doc %{gem_instdir rdoc}/TODO.rdoc

%if %{with batteries}
%files rubygems
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gem
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb

%files bundler
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bundler
%attr(755,root,root) %{_bindir}/bundle
%{gem_instdir bundler}
%{gem_spec bundler}

%files rake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rake
%dir %{gem_instdir rake}
%{gem_instdir rake}/lib
%{gem_spec rake}
%{gem_instdir rake}/rake.gemspec
%dir %{gem_instdir rake}/exe
%attr(755,root,root) %{gem_instdir rake}/exe/rake

%files json
%defattr(644,root,root,755)
%{ruby_libdir}/json
%dir %{ruby_archdir}/json
%dir %{ruby_archdir}/json/ext
%{ruby_archdir}/json/ext/*.so

%dir %{gem_extdir_mri json}
%{gem_extdir_mri json}/gem.build_complete
%dir %{gem_extdir_mri json}/lib
%dir %{gem_extdir_mri json}/lib/json
%dir %{gem_extdir_mri json}/lib/json/ext
%{gem_extdir_mri json}/lib/json/ext/generator.so
%{gem_extdir_mri json}/lib/json/ext/parser.so

%{gem_instdir json}
%{gem_spec json}
%endif

%files power_assert
%defattr(644,root,root,755)
%dir %{gem_instdir power_assert}
%{gem_instdir power_assert}/lib
%{gem_spec power_assert}

%files minitest
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/minitest
%{ruby_libdir}/minitest
%{gem_instdir minitest}
%{gem_spec minitest}

%files test-unit
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/test-unit
%dir %{gem_instdir test-unit}
%{gem_instdir test-unit}/bin
%{gem_instdir test-unit}/lib
%{gem_spec test-unit}
%{_mandir}/man1/testrb.1*

%files racc
%defattr(644,root,root,755)
%dir %{gem_instdir racc}
%dir %{gem_extdir_mri racc}
%{gem_extdir_mri racc}/gem.build_complete
%dir %{gem_extdir_mri racc}/racc
%attr(755,root,root) %{gem_extdir_mri racc}/racc/cparse.so
%attr(755,root,root) %{_bindir}/racc
%{gem_instdir racc}/bin
%{gem_instdir racc}/lib
%{gem_spec racc}

%files rbs
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rbs
%dir %{gem_extdir_mri rbs}
%{gem_extdir_mri rbs}/gem.build_complete
%attr(755,root,root) %{gem_extdir_mri rbs}/rbs_extension.so
%{gem_instdir rbs}
%exclude %{gem_instdir rbs}/.*
%{gem_spec rbs}

%files typeprof
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/typeprof
%{gem_instdir typeprof}
%exclude %{gem_instdir typeprof}/.*
%{gem_spec typeprof}

%files bigdecimal
%defattr(644,root,root,755)
%{gem_instdir bigdecimal}
%{gem_extdir_mri bigdecimal}
%{gem_spec bigdecimal}
%{ruby_libdir}/bigdecimal
%{ruby_libdir}/bigdecimal.rb
%{ruby_archdir}/bigdecimal.so

%files io-console
%defattr(644,root,root,755)
%{gem_instdir io-console}
%dir %{gem_extdir_mri io-console}
%{gem_extdir_mri io-console}/gem.build_complete
%dir %{gem_extdir_mri io-console}/lib
%dir %{gem_extdir_mri io-console}/lib/io
%{gem_extdir_mri io-console}/lib/io/console.so
%{gem_spec io-console}

%files psych
%defattr(644,root,root,755)
%{ruby_libdir}/psych.rb
%{ruby_archdir}/psych.so
%{gem_instdir psych}
%{ruby_libdir}/psych
%dir %{gem_extdir_mri psych}
%{gem_extdir_mri psych}/gem.build_complete
%dir %{gem_extdir_mri psych}/lib
%{gem_extdir_mri psych}/lib/psych.so
%{gem_spec psych}

%files rexml
%defattr(644,root,root,755)
%dir %{gem_instdir rexml}
%{gem_instdir rexml}/lib
%{gem_spec rexml}

%files rss
%defattr(644,root,root,755)
%dir %{gem_instdir rss}
%{gem_instdir rss}/lib
%{gem_spec rss}

%files bundled-gems
%defattr(644,root,root,755)
# abbrev
%dir %{gem_instdir abbrev}
%doc %{gem_instdir abbrev}/LICENSE.txt
%{gem_instdir abbrev}/bin
%{gem_instdir abbrev}/lib
%{gem_spec abbrev}
%{gem_instdir abbrev}/Gemfile
%doc %{gem_instdir abbrev}/README.md
%{gem_instdir abbrev}/Rakefile

# base64
%dir %{gem_instdir base64}
%license %{gem_instdir base64}/BSDL
%license %{gem_instdir base64}/COPYING
%license %{gem_instdir base64}/LEGAL
%{gem_instdir base64}/lib
%{gem_spec base64}
%doc %{gem_instdir base64}/README.md
%doc %{gem_instdir base64}/sig

# benchmark
%dir %{gem_instdir benchmark}
%license %{gem_instdir benchmark}/BSDL
%license %{gem_instdir benchmark}/COPYING
%{gem_instdir benchmark}/bin
%{gem_instdir benchmark}/lib
%{gem_spec benchmark}
%{gem_instdir benchmark}/Gemfile
%doc %{gem_instdir benchmark}/README.md
%{gem_instdir benchmark}/Rakefile

# fiddle
%dir %{gem_instdir fiddle}
%dir %{gem_extdir_mri fiddle}
%{gem_extdir_mri fiddle}/gem.build_complete
%attr(755,root,root) %{gem_extdir_mri fiddle}/fiddle.so
%{gem_instdir fiddle}/lib
%{gem_spec fiddle}
%{gem_instdir fiddle}/fiddle.gemspec
%doc %{gem_instdir fiddle}/LICENSE.txt
%doc %{gem_instdir fiddle}/README.md
%{gem_instdir fiddle}/Rakefile

# logger
%dir %{gem_instdir logger}
%license %{gem_instdir logger}/BSDL
%license %{gem_instdir logger}/COPYING
%{gem_instdir logger}/lib
%{gem_spec logger}
%doc %{gem_instdir logger}/README.md

# ostruct
%dir %{gem_instdir ostruct}
%license %{gem_instdir ostruct}/BSDL
%license %{gem_instdir ostruct}/COPYING
%{gem_instdir ostruct}/bin
%{gem_instdir ostruct}/lib
%{gem_spec ostruct}
%{gem_instdir ostruct}/ostruct.gemspec
%{gem_instdir ostruct}/Gemfile
%doc %{gem_instdir ostruct}/README.md
%{gem_instdir ostruct}/Rakefile

# pstore
%dir %{gem_instdir pstore}
%license %{gem_instdir pstore}/BSDL
%license %{gem_instdir pstore}/COPYING
%{gem_instdir pstore}/bin
%{gem_instdir pstore}/lib
%{gem_spec pstore}
%{gem_instdir pstore}/Gemfile
%doc %{gem_instdir pstore}/README.md
%{gem_instdir pstore}/Rakefile

# csv
%dir %{gem_instdir csv}
%doc %{gem_instdir csv}/LICENSE.txt
%doc %{gem_instdir csv}/NEWS.md
%{gem_instdir csv}/lib
%{gem_spec csv}
%doc %{gem_instdir csv}/README.md
%doc %{gem_instdir csv}/doc

# drb
%dir %{gem_instdir drb}
%doc %{gem_instdir drb}/LICENSE.txt
%{gem_instdir drb}/lib
%{gem_spec drb}
%{gem_instdir drb}/drb.gemspec

# getoptlong
%dir %{gem_instdir getoptlong}
%doc %{gem_instdir getoptlong}/LICENSE.txt
%{gem_instdir getoptlong}/bin
%{gem_instdir getoptlong}/lib
%{gem_instdir getoptlong}/sample
%{gem_spec getoptlong}
%{gem_instdir getoptlong}/Gemfile
%doc %{gem_instdir getoptlong}/README.md
%{gem_instdir getoptlong}/Rakefile

# matrix
%dir %{gem_instdir matrix}
%{gem_instdir matrix}/lib
%{gem_spec matrix}
%{gem_instdir matrix}/matrix.gemspec

# mutex_m
%dir %{gem_instdir mutex_m}
%doc %{gem_instdir mutex_m}/BSDL
%doc %{gem_instdir mutex_m}/COPYING
%{gem_instdir mutex_m}/lib
%{gem_instdir mutex_m}/sig
%{gem_spec mutex_m}
%doc %{gem_instdir mutex_m}/README.md

# net-ftp
%dir %{gem_instdir net-ftp}
%{gem_instdir net-ftp}/lib
%{gem_spec net-ftp}

# net-imap
%dir %{gem_instdir net-imap}
%{gem_instdir net-imap}/lib
%{gem_instdir net-imap}/rakelib
%{gem_instdir net-imap}/sample
%{gem_spec net-imap}

# net-pop
%dir %{gem_instdir net-pop}
%{gem_instdir net-pop}/lib
%{gem_spec net-pop}

# net-smtp
%dir %{gem_instdir net-smtp}
%{gem_instdir net-smtp}/lib
%{gem_spec net-smtp}

# nkf
%dir %{gem_instdir nkf}
%{gem_extdir_mri nkf}
%doc %{gem_instdir nkf}/LICENSE.txt
%{gem_instdir nkf}/bin
%{gem_instdir nkf}/lib
%{gem_spec nkf}
%{gem_instdir nkf}/Gemfile
%doc %{gem_instdir nkf}/README.md
%{gem_instdir nkf}/Rakefile

# observer
%dir %{gem_instdir observer}
%doc %{gem_instdir observer}/LICENSE.txt
%{gem_instdir observer}/bin
%{gem_instdir observer}/lib
%{gem_spec observer}
%{gem_instdir observer}/Gemfile
%doc %{gem_instdir observer}/README.md
%{gem_instdir observer}/Rakefile

# readline
%dir %{gem_instdir readline}
%license %{gem_instdir readline}/BSDL
%license %{gem_instdir readline}/COPYING
%{gem_instdir readline}/lib
%{gem_spec readline}
%doc %{gem_instdir readline}/README.md

# reline
%dir %{gem_instdir reline}
%license %{gem_instdir reline}/BSDL
%license %{gem_instdir reline}/COPYING
%{gem_instdir reline}/lib
%{gem_spec reline}
%doc %{gem_instdir reline}/README.md
%{gem_instdir reline}/license_of_rb-readline

# prime
%dir %{gem_instdir prime}
%{gem_instdir prime}/lib
%{gem_instdir prime}/sig
%{gem_spec prime}
%{gem_instdir prime}/prime.gemspec

# rdbg
%attr(755,root,root) %{_bindir}/rdbg
%dir %{gem_extdir_mri debug}
%{gem_extdir_mri debug}/gem.build_complete
%dir %{gem_extdir_mri debug}/debug
%{gem_extdir_mri debug}/debug/debug.so
%dir %{gem_instdir debug}
%exclude %{gem_instdir debug}/.*
%{gem_instdir debug}/exe
%{gem_instdir debug}/lib
%{gem_spec debug}

# repl_type_completor
%dir %{gem_instdir repl_type_completor}
%doc %{gem_instdir repl_type_completor}/LICENSE.txt
%{gem_instdir repl_type_completor}/lib
%{gem_instdir repl_type_completor}/sig
%{gem_spec repl_type_completor}
%{gem_instdir repl_type_completor}/Gemfile
%doc %{gem_instdir repl_type_completor}/README.md
%{gem_instdir repl_type_completor}/Rakefile

# rinda
%dir %{gem_instdir rinda}
%doc %{gem_instdir rinda}/LICENSE.txt
%{gem_instdir rinda}/bin
%{gem_instdir rinda}/lib
%{gem_spec rinda}
%{gem_instdir rinda}/Gemfile
%doc %{gem_instdir rinda}/README.md
%{gem_instdir rinda}/Rakefile

# resolv-replace
%dir %{gem_instdir resolv-replace}
%doc %{gem_instdir resolv-replace}/LICENSE.txt
%{gem_instdir resolv-replace}/bin
%{gem_instdir resolv-replace}/lib
%{gem_spec resolv-replace}
%{gem_instdir resolv-replace}/Gemfile
%doc %{gem_instdir resolv-replace}/README.md
%{gem_instdir resolv-replace}/Rakefile

# syslog
%dir %{gem_instdir syslog}
%{gem_extdir_mri syslog}
%{gem_instdir syslog}/bin
%{gem_instdir syslog}/lib
%{gem_spec syslog}

%files modules
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/erb
%attr(755,root,root) %{_bindir}/syntax_suggest
%{gem_instdir syntax_suggest}
%{ruby_libdir}/bundled_gems.rb
%{ruby_libdir}/cgi
%{ruby_libdir}/digest
%{ruby_libdir}/io
%{ruby_libdir}/net
%{ruby_libdir}/openssl
%{ruby_libdir}/optparse
%{ruby_libdir}/ripper
%{ruby_libdir}/test
%{ruby_libdir}/uri
%{ruby_libdir}/yaml
%{ruby_libdir}/English.rb
%{ruby_libdir}/bundler
%{ruby_libdir}/bundler.rb
%{ruby_libdir}/cgi.rb
%{ruby_libdir}/coverage.rb
%{ruby_libdir}/date.rb
%{ruby_libdir}/delegate.rb
%{ruby_libdir}/did_you_mean.rb
%{ruby_libdir}/did_you_mean
%{ruby_libdir}/digest.rb
%{ruby_libdir}/error_highlight.rb
%dir %{ruby_libdir}/error_highlight
%{ruby_libdir}/error_highlight/*.rb
%{ruby_libdir}/erb.rb
%dir %{ruby_libdir}/erb
%{ruby_libdir}/erb/*.rb
%{ruby_libdir}/expect.rb
%{ruby_libdir}/fileutils.rb
%{ruby_libdir}/find.rb
%{ruby_libdir}/forwardable.rb
%dir %{ruby_libdir}/forwardable
%{ruby_libdir}/forwardable/impl.rb
%{ruby_libdir}/ipaddr.rb
%{ruby_libdir}/json.rb
%{ruby_libdir}/monitor.rb
%{ruby_libdir}/objspace.rb
%dir %{ruby_libdir}/objspace
%{ruby_libdir}/objspace/*.rb
%{ruby_libdir}/open-uri.rb
%{ruby_libdir}/open3.rb
%dir %{ruby_libdir}/open3
%{ruby_libdir}/open3/version.rb
%{ruby_libdir}/openssl.rb
%{ruby_libdir}/optionparser.rb
%{ruby_libdir}/optparse.rb
%{ruby_libdir}/pathname.rb
%{ruby_libdir}/pp.rb
%{ruby_libdir}/prettyprint.rb
%{ruby_libdir}/prism*
%dir %{ruby_libdir}/random
%{ruby_libdir}/random/*.rb
%{ruby_libdir}/rdoc.rb

%{ruby_libdir}/resolv.rb
%{ruby_libdir}/ripper.rb
%{ruby_libdir}/securerandom.rb
%dir %{ruby_libdir}/set
%{ruby_libdir}/set/subclass_compatible.rb
%{ruby_libdir}/shellwords.rb
%{ruby_libdir}/singleton.rb
%{ruby_libdir}/socket.rb
%dir %{ruby_libdir}/strscan
%{ruby_libdir}/strscan/*.rb
%{ruby_libdir}/syntax_suggest.rb
%dir %{ruby_libdir}/syntax_suggest
%{ruby_libdir}/syntax_suggest/*.rb
%dir %{ruby_libdir}/syntax_suggest/capture
%{ruby_libdir}/syntax_suggest/capture/*.rb
%{ruby_libdir}/tempfile.rb
%{ruby_libdir}/time.rb
%{ruby_libdir}/timeout.rb
%{ruby_libdir}/tmpdir.rb
%{ruby_libdir}/tsort.rb
%{ruby_libdir}/un.rb
%{ruby_libdir}/unicode_normalize
%{ruby_libdir}/uri.rb
%{ruby_libdir}/weakref.rb
%{ruby_libdir}/yaml.rb

%if %{with batteries}
%exclude %{ruby_libdir}/rubygems.rb
%endif
%exclude %{ruby_libdir}/mkmf.rb

%{ruby_archdir}/rbconfig.rb
%attr(755,root,root) %{ruby_archdir}/continuation.so
%attr(755,root,root) %{ruby_archdir}/coverage.so
%attr(755,root,root) %{ruby_archdir}/date_core.so
%attr(755,root,root) %{ruby_archdir}/digest.so
%attr(755,root,root) %{ruby_archdir}%{_sysconfdir}.so
%attr(755,root,root) %{ruby_archdir}/erb/escape.so
%attr(755,root,root) %{ruby_archdir}/fcntl.so
%attr(755,root,root) %{ruby_archdir}/monitor.so
%attr(755,root,root) %{ruby_archdir}/objspace.so
%attr(755,root,root) %{ruby_archdir}/openssl.so
%attr(755,root,root) %{ruby_archdir}/pty.so
%attr(755,root,root) %{ruby_archdir}/ripper.so
%attr(755,root,root) %{ruby_archdir}/socket.so
%attr(755,root,root) %{ruby_archdir}/stringio.so
%attr(755,root,root) %{ruby_archdir}/strscan.so
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
%{ruby_archdir}/io/*.so
%dir %{ruby_archdir}/rbconfig
%attr(755,root,root) %{ruby_archdir}/rbconfig/sizeof.so

%dir %{_libdir}/gems
%dir %{_libdir}/gems/%{oname}

%dir %{gem_dir}
%dir %{gem_dir}/gems
# for libexec/erb
%{gem_instdir erb}

%dir %{gem_dir}/specifications
%dir %{gem_dir}/specifications/default
%{gem_dir}/specifications/default/*.gemspec

%{_mandir}/man1/erb.1*

%if %{with doc}
# Since RDoc 7 the ri data is versioned below %%{_datadir}/ri/%%{ruby_version},
# so take the whole tree rather than listing individual files.  The empty
# %%{_datadir}/rdoc is already owned by the main ruby package.
%files doc-ri
%defattr(644,root,root,755)
%{_datadir}/ri
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{oname}-%{pkg_version}
