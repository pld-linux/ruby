# TODO:
#	- include ext/ in docs
#	- replace ri with fastri
#	- patch ri to search multiple indexes (one per package), so RPMs can install ri docs
#	- gemify irb (?)
#
# Conditional build:
%bcond_without	doc		# skip (time-consuming) docs generating; intended for speed up test builds
%bcond_without	batteries	# Don't include rubygems, json, rake, minitest
%bcond_without	default_ruby	# use this Ruby as default system Ruby
%bcond_without	dtrace		# disable tracing with dtrace
%bcond_with	bootstrap	# build bootstrap version
%bcond_with	tests		# build without tests

%define		rel		4
%define		ruby_version	2.6
%define		patchlevel	10
%define		pkg_version	%{ruby_version}.%{patchlevel}
%define		ruby_suffix %{!?with_default_ruby:%{ruby_version}}
%define		doc_version	2_6_9
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
# Source0-md5:	de4cf1c977d6dd05b9842015a9a21efd
Source2:	https://www.ruby-doc.org/downloads/%{oname}_%{doc_version}_stdlib_rdocs.tgz
# Source2-md5:	f726a5bd96f90969fb15b1e785375af5
Source3:	https://www.ruby-doc.org/downloads/%{oname}_%{doc_version}_core_rdocs.tgz
# Source3-md5:	53251c65f70f6e4e37ca0451b6268cac
Source50:	https://www.unicode.org/Public/9.0.0/ucd/CaseFolding.txt
# Source50-md5:	e3fbf2f626f10070000fe66f3a2ff5ef
Source51:	https://www.unicode.org/Public/9.0.0/ucd/CompositionExclusions.txt
# Source51-md5:	263381d7b4b5e2d52a91e1bbbd4722d4
Source52:	https://www.unicode.org/Public/9.0.0/ucd/NormalizationTest.txt
# Source52-md5:	aacb8a8acfc449d09136fe39f3f97cf1
Source53:	https://www.unicode.org/Public/9.0.0/ucd/SpecialCasing.txt
# Source53-md5:	fea30f45a2f81ffa474fd984d297e2ea
Source54:	https://www.unicode.org/Public/9.0.0/ucd/UnicodeData.txt
# Source54-md5:	dde25b1cf9bbb4ba1140ac12e4128b0b
Source4:	rdoc.1
Source5:	testrb.1
Source6:	operating_system.rb
Patch0:		autoconf2.70.patch
Patch1:		bison3.59.patch
Patch2:		fix-bison-invocation.patch
Patch3:		mkmf-verbose.patch
Patch4:		strip-ccache.patch
Patch5:		ruby-version.patch
Patch6:		duplicated-paths.patch
Patch7:		openssl3.patch
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
BuildRequires:	rpmbuild(macros) >= 1.527
# which version is minimum now? 1.8.7 is not enough, fails with:
# ./tool/generic_erb.rb:31: syntax error, unexpected ':', expecting ')'
# ...O.popen("tput smso", "r", err: IO::NULL, &:read) rescue nil)
BuildRequires:	ruby >= 1:1.9
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
Obsoletes:	ruby-REXML <= 2.4.0-2
Obsoletes:	ruby-doc < 1.8.4
Obsoletes:	ruby-fastthread <= 0.6.3
Conflicts:	rpm-build-macros < 1.695
Conflicts:	ruby-activesupport < 2.3.11-2
Conflicts:	ruby-activesupport2 < 2.3.11-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# hack: skip rubygem(ipaddr)
%define	_noautoreq	ipaddr

# separate modules
%define	bigdecimal_ver		1.4.1
%define	bundler_ver		1.17.2
%define	did_you_mean_ver	1.3.0
%define	io_console_ver		0.4.7
%define	irb_ver			1.0.0
%define	json_ver		2.1.0
%define	minitest_ver		5.11.3
%define	net_telnet_ver		0.2.0
%define	power_assert_ver	1.1.3
%define	psych_ver		3.1.0
%define	rake_ver		12.3.3
%define	rdoc_ver		6.1.2.1
%define	rubygems_ver		3.0.3.1
%define	test_unit_ver		3.2.9
%define	xmlrpc_ver		0.3.0
# default modules, separated
%define	irb_ver			1.0.0
# default modules packaged in main modules
%define	cmath_ver		1.0.0
%define	csv_ver			3.0.9
%define	date_ver		2.0.3
%define	dbm_ver			1.0.0
%define	e2mmap_ver		0.1.0
%define	etc_ver			1.0.1
%define	fcntl_ver		1.0.0
%define	fiddle_ver		1.0.0
%define	fileutils_ver		1.1.0
%define	forwardable_ver		1.2.0
%define	gdbm_ver		2.0.0
%define	ipaddr_ver		1.2.2
%define	logger_ver		1.3.0
%define	matrix_ver		0.1.0
%define	mutex_m_ver		0.1.0
%define	ostruct_ver		0.1.0
%define	openssl_ver		2.1.2
%define	prime_ver		0.1.0
%define	rexml_ver		3.1.9.1
%define	rss_ver			0.2.7
%define	scanf_ver		1.0.0
%define	sdbm_ver		1.0.0
%define	shell_ver		0.7
%define	stringio_ver		0.0.2
%define	strscan_ver		1.0.0
%define	sync_ver		0.5.0
%define	thwait_ver		0.1.0
%define	tracer_ver		0.1.0
%define	webrick_ver		1.4.4
%define	zlib_ver		1.0.0

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
Obsoletes:	ruby-static < 1:2.4

%description devel
Ruby development libraries.

%description devel -l pl.UTF-8
Biblioteki programistyczne interpretera języka Ruby.

%package doc
Summary:	Ruby HTML documentation
Summary(pl.UTF-8):	Dokumentacja HTML do Ruby
Group:		Documentation
BuildArch:	noarch

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
BuildArch:	noarch

%description doc-ri
Ruby ri documentation.

%description doc-ri -l pl.UTF-8
Dokumentacja Ruby w formacie ri.

%package examples
Summary:	Ruby examples
Summary(pl.UTF-8):	Przykłady dla języka Ruby
Group:		Development/Languages
BuildArch:	noarch

%description examples
Ruby examples.

%description examples -l pl.UTF-8
Przykłady programów w języku Ruby.

# IMPORTANT: keep irb, rdoc, rubygems, rake, json as last packages as we reset epoch/version/release
# and %{version},%{release} macros may not be used directly as they take last
# subpackage value not main package one what you intend to use

%package irb
Summary:	The Interactive Ruby
Summary(pl.UTF-8):	Interaktywny Ruby
Version:	%{irb_ver}
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
BuildArch:	noarch

%description rubygems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%description rubygems -l pl.UTF-8
RubyGems to standardowe narzędzie języka Ruby do publikowania i
zarządzania zewnętrznymi bibliotekami.

%package bundler
Summary:	Library and utilities to manage a Ruby application's gem dependencies
Summary(pl.UTF-8):	Biblioteka i narzędzia do zarządzania zależnościami gem aplikacji w języku Ruby
Version:	%{bundler_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Languages
Provides:	bundler = %{bundler_ver}
BuildArch:	noarch

%description bundler
Bundler manages an application's dependencies through its entire life,
across many machines, systematically and repeatably.

%description bundler -l pl.UTF-8
Bundler zarządza zależnościami aplikacji przez cały czas jej życia,
między wiloma maszynami - systematycznie i powtarzalnie.

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
Summary(pl.UTF-8):	Biblioteka JSON dla języka Ruby
Version:	%{json_ver}
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
Summary(pl.UTF-8):	Minitest - kompletny szkielet do testowania
Version:	%{minitest_ver}
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
Summary(pl.UTF-8):	Power Assert dla języka Ruby
Version:	%{power_assert_ver}
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
Summary(pl.UTF-8):	Szkielet testów z rodziny xUnit dla języka Ruby
Version:	%{test_unit_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
# lib/test/unit/diff.rb is a double license of the Ruby license and PSF license.
# lib/test-unit.rb is a dual license of the Ruby license and LGPLv2.1 or later.
License:	(Ruby or BSD) and (Ruby or BSD or Python) and (Ruby or BSD or LGPL v2+)
Group:		Development/Libraries
Requires:	ruby-power_assert = %{power_assert_ver}-%{pkg_version}.%{rel}
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

%package did_you_mean
Summary:	"Did you mean?" experience in Ruby
Summary(pl.UTF-8):	Zachowanie "czy miałeś na myśli?" w języku Ruby
Version:	%{did_you_mean_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries
BuildArch:	noarch

%description did_you_mean
"Did you mean?" experience in Ruby: the error message will tell you
the right one when you misspelled something.

%description did_you_mean -l pl.UTF-8
Zachowanie "czy miałeś na myśli" w języku ruby: komunikat błędu
podpowie właściwą pisownię w przypadku literówki.

%package net-telnet
Summary:	Provides telnet client functionality
Summary(pl.UTF-8):	Funkcjonalność klienta usługi telnet
Version:	%{net_telnet_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
Group:		Development/Libraries
BuildArch:	noarch

%description net-telnet
Provides telnet client functionality.

This class also has, through delegation, all the methods of a socket
object (by default, a TCPSocket, but can be set by the Proxy option to
new()). This provides methods such as close() to end the session and
sysread() to read data directly from the host, instead of via the
waitfor() mechanism.

%description net-telnet -l pl.UTF-8
Ten pakiet dostarcza funkcjonalność klienta usługi telnet.

Ta klasa ma, poprzez delegację, wszystkie metody obiektu gniazda
(domyślnie TCPSocket, ale może być ustawiona przez opcję Proxy dla
new()). Udostępnia metody takie jak: close() do zakończenia sesji czy
sysread() do odczytu danych bezpośrednio z hosta zamiast poprzez
mechanizm waitfor().

%package bigdecimal
Summary:	BigDecimal - arbitrary-precision floating point decimal arithmetic
Summary(pl.UTF-8):	BigDecimal - dziesiętna arytmetyka zmiennoprzecinkowa o dowolnej dokładności
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
Summary(pl.UTF-8):	IO/Console - prosta biblioteka wykorzystująca konsolę
Version:	%{io_console_ver}
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
Summary(pl.UTF-8):	Obudowanie libyaml dla języka Ruby
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

%description psych -l pl.UTF-8
Psych to parser i emiter YAML. Wykorzystuje libyaml do analizy i
emitowania YAML-a. Poza obudowaniem libyaml, wie także jak
serializować i deserializować większość obiektów języka Ruby do/z
formatu YAML.

%package xmlrpc
Summary:	A xmlrpc wrapper for Ruby
Summary(pl.UTF-8):	Obudowanie xmlrpc dla języka Ruby
Version:	%{xmlrpc_ver}
Release:	%{pkg_version}.%{rel}
Epoch:		0
License:	MIT
Group:		Development/Libraries

%description xmlrpc
XMLRPC is a lightweight protocol that enables remote procedure calls
over HTTP. It is defined at <http://www.xmlrpc.com/>.

XMLRPC allows you to create simple distributed computing solutions
that span computer languages. Its distinctive feature is its
simplicity compared to other approaches like SOAP and CORBA.

The Ruby standard library package 'xmlrpc' enables you to create a
server that implements remote procedures and a client that calls them.
Very little code is required to achieve either of these.

%description xmlrpc -l pl.UTF-8
XMLRPC to lekki protokół pozwalający na wywołania zdalnych procedur
poprzez HTTP. Jest zdefiniowany na <http://www.xmlrpc.com/>.

XMLRPC pozwala na tworzenie prostych, rozproszonych systemów
komputerowych dla wielu języków. Wyróżniającą cechą jest prostota w
porównaniu do innych rozwiązań, takich jak SOAP czy CORBA.

Pakiet biblioteki standardowej języka Ruby 'xmlrpc' pozwala na
stworzenie serwera implementującego procedury zdalne oraz klienta
wywołującego je. Aby to osiągnąć wystarczy bardzo mało kodu.

%prep
%setup -q -n %{oname}-%{pkg_version} -a2 -a3
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
#%%patch8 -p1
%patch -P9 -p1
%patch -P12 -p1

install -d enc/unicode/data/9.0.0
cp -p %{SOURCE50} %{SOURCE51} %{SOURCE52} %{SOURCE53} %{SOURCE54} enc/unicode/data/9.0.0/

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

%if %{with bootstrap}
# avoid regeneration, needs iostring module
touch enc/unicode/9.0.0/*.h
%endif

%build
rubygems_ver=$(awk '/VERSION =/ && $1 == "VERSION" {print $3}' lib/rubygems.rb | sed 's/\.freeze//g' | xargs)
if [ $rubygems_ver != %{rubygems_ver} ]; then
	echo "Set %%define rubygems_ver to $rubygems_ver and re-run."
	exit 1
fi
rdoc_ver=$(awk '/VERSION =/ && $1 == "VERSION" {print $3}' lib/rdoc/version.rb | xargs)
if [ "$rdoc_ver" != %{rdoc_ver} ]; then
	echo "Set %%define rdoc_ver to $rdoc_ver and re-run."
	exit 1
fi

cp -f /usr/share/automake/config.sub .

%{__autoconf}
%configure \
	%{?with_bootstrap:--with-baseruby="%{_bindir}/ruby -I$(pwd)/lib"} \
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
	--without-compress-debug-sections \
	--enable-multiarch \
	--enable-shared \
	--disable-install-doc \
	--disable-rpath \
	--disable-rubygems \
	%{__enable_disable dtrace} \
	--with-ruby-version='' \

%{__make} -j1 main \
	COPY="cp -p" \
	V=1

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
install -d $RPM_BUILD_ROOT%{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/bigdecimal $RPM_BUILD_ROOT%{gem_dir}/gems/bigdecimal-%{bigdecimal_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal.so $RPM_BUILD_ROOT%{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal/util.so $RPM_BUILD_ROOT%{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal/
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/bigdecimal-%{bigdecimal_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal $RPM_BUILD_ROOT%{ruby_libdir}/bigdecimal
ln -s %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal.so $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal.so
install -d $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal
ln -s %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal/util.so $RPM_BUILD_ROOT%{ruby_libarchdir}/bigdecimal/util.so

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
ln -s %{gem_dir}/gems/test-unit-%{test_unit_ver}/lib/test/unit $RPM_BUILD_ROOT%{ruby_libdir}/test

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/psych-%{psych_ver}/lib
install -d $RPM_BUILD_ROOT%{gem_libdir}/psych-%{psych_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/psych* $RPM_BUILD_ROOT%{gem_dir}/gems/psych-%{psych_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libarchdir}/psych.so $RPM_BUILD_ROOT%{gem_libdir}/psych-%{psych_ver}/lib/
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/psych-%{psych_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/psych-%{psych_ver}/lib/psych $RPM_BUILD_ROOT%{ruby_libdir}/psych
ln -s %{gem_dir}/gems/psych-%{psych_ver}/lib/psych.rb $RPM_BUILD_ROOT%{ruby_libdir}/psych.rb
ln -s %{gem_libdir}/psych-%{psych_ver}/lib/psych.so $RPM_BUILD_ROOT%{ruby_archdir}/psych.so

install -d $RPM_BUILD_ROOT%{gem_dir}/gems/bundler-%{bundler_ver}/lib
install -d $RPM_BUILD_ROOT%{gem_libdir}/bundler-%{bundler_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{ruby_libdir}/bundler* $RPM_BUILD_ROOT%{gem_dir}/gems/bundler-%{bundler_ver}/lib
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/specifications/default/bundler-%{bundler_ver}.gemspec $RPM_BUILD_ROOT%{gem_dir}/specifications
ln -s %{gem_dir}/gems/bundler-%{bundler_ver}/lib/bundler $RPM_BUILD_ROOT%{ruby_libdir}/bundler
ln -s %{gem_dir}/gems/bundler-%{bundler_ver}/lib/bundler.rb $RPM_BUILD_ROOT%{ruby_libdir}/bundler.rb

# replace default irb with its not gemified version
%{__mv} $RPM_BUILD_ROOT%{gem_dir}/gems/irb-%{irb_ver}/exe/irb $RPM_BUILD_ROOT%{_bindir}/irb%{ruby_suffix}

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
	%{__make} runruby TESTRUN_SCRIPT="-rrubygems \
	-e \"spec = Gem::Specification.load('$s')\" \
	-e \"File.write '$s', spec.to_ruby\""
done

%{__sed} -i -e '1s,/usr/bin/env ruby,/usr/bin/ruby,' \
 	$RPM_BUILD_ROOT%{_bindir}/irb \
	$RPM_BUILD_ROOT%{ruby_libdir}/abbrev.rb \
	$RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/exe/rake \
	$RPM_BUILD_ROOT%{gem_dir}/gems/rdoc-%{rdoc_ver}/exe/{rdoc,ri} \
	$RPM_BUILD_ROOT%{gem_dir}/gems/bundler-%{bundler_ver}/exe/{bundle,bundler} \
	$RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}/{cal,test,time,uumerge}.rb \
	$RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}/{drb,logger,openssl,ripper,rss}/*.rb \
	$RPM_BUILD_ROOT%{_examplesdir}/%{oname}-%{pkg_version}/webrick/*.cgi

# gem non library files
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/did_you_mean-%{did_you_mean_ver}/{[A-Z]*,benchmark,doc,test,tmp,did_you_mean.gemspec,.*}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/minitest-%{minitest_ver}/{[A-Z]*,test,.autotest}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/net-telnet-%{net_telnet_ver}/{[A-Z]*,bin,net-telnet.gemspec,.*}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/power_assert-%{power_assert_ver}/{[A-Z]*,bin,power_assert.gemspec,.*}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/rake-%{rake_ver}/{[A-Z]*,bin,doc,rake.gemspec,azure-pipelines.yml}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/test-unit-%{test_unit_ver}/{[A-Z]*,doc,sample,test}
%{__rm} -r $RPM_BUILD_ROOT%{gem_dir}/gems/xmlrpc-%{xmlrpc_ver}/{[A-Z]*,bin,xmlrpc.gemspec,.*}

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
%{__rm} $RPM_BUILD_ROOT%{ruby_ridir}/win32/page-*.ri
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
%{gem_dir}/specifications/default/irb-%{irb_ver}.gemspec
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
%dir %{gem_dir}/gems/rdoc-%{rdoc_ver}/exe
%{gem_dir}/gems/rdoc-%{rdoc_ver}/exe/rdoc
%{gem_dir}/gems/rdoc-%{rdoc_ver}/exe/ri

%if %{with batteries}
%files rubygems
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gem%{ruby_suffix}
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb

%files bundler
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/bundler%{ruby_suffix}
%attr(755,root,root) %{_bindir}/bundle%{ruby_suffix}
%{gem_dir}/gems/bundler-%{bundler_ver}
%{gem_dir}/specifications/bundler-%{bundler_ver}.gemspec
%{_mandir}/man1/bundle*.1*
%{_mandir}/man5/gemfile.5*

%files rake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rake%{ruby_suffix}
%dir %{gem_dir}/gems/rake-%{rake_ver}
%{gem_dir}/gems/rake-%{rake_ver}/lib
%{gem_dir}/specifications/rake-%{rake_ver}.gemspec
%dir %{gem_dir}/gems/rake-%{rake_ver}/exe
%attr(755,root,root) %{gem_dir}/gems/rake-%{rake_ver}/exe/rake

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
%dir %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal
%attr(755,root,root) %{gem_libdir}/bigdecimal-%{bigdecimal_ver}/lib/bigdecimal/util.so
%{ruby_libdir}/bigdecimal.rb
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
%{gem_dir}/gems/xmlrpc-%{xmlrpc_ver}
%{gem_dir}/specifications/xmlrpc-%{xmlrpc_ver}.gemspec

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
%{ruby_libdir}/bundler
%{ruby_libdir}/bundler.rb
%{ruby_libdir}/cgi.rb
%{ruby_libdir}/cmath.rb
%{ruby_libdir}/csv.rb
%{ruby_libdir}/csv
%{ruby_libdir}/coverage.rb
%{ruby_libdir}/date.rb
%{ruby_libdir}/debug.rb
%{ruby_libdir}/delegate.rb
%{ruby_libdir}/digest.rb
%{ruby_libdir}/drb.rb
%{ruby_libdir}/e2mmap.rb
%{ruby_libdir}/e2mmap
%{ruby_libdir}/erb.rb
%{ruby_libdir}/expect.rb
%{ruby_libdir}/fiddle.rb
%{ruby_libdir}/fileutils.rb
%{ruby_libdir}/fileutils
%{ruby_libdir}/find.rb
%{ruby_libdir}/forwardable.rb
%dir %{ruby_libdir}/forwardable
%{ruby_libdir}/forwardable/impl.rb
%{ruby_libdir}/getoptlong.rb
%{ruby_libdir}/ipaddr.rb
%{ruby_libdir}/json.rb
%{ruby_libdir}/kconv.rb
%{ruby_libdir}/logger.rb
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
%{ruby_libdir}/thwait
%{ruby_libdir}/time.rb
%{ruby_libdir}/timeout.rb
%{ruby_libdir}/tmpdir.rb
%{ruby_libdir}/tracer.rb
%{ruby_libdir}/tracer
%{ruby_libdir}/tsort.rb
%{ruby_libdir}/un.rb
%{ruby_libdir}/unicode_normalize
%{ruby_libdir}/uri.rb
%{ruby_libdir}/weakref.rb
%{ruby_libdir}/webrick.rb
%{ruby_libdir}/yaml.rb

%if %{with batteries}
%exclude %{ruby_libdir}/rubygems.rb
%endif
%exclude %{ruby_libdir}/irb.rb
%exclude %{ruby_libdir}/mkmf.rb

%{ruby_archdir}/rbconfig.rb
%attr(755,root,root) %{ruby_archdir}/bigdecimal.so
%dir %{ruby_archdir}/bigdecimal
%attr(755,root,root) %{ruby_archdir}/bigdecimal/util.so
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
%{gem_dir}/specifications/default/cmath-%{cmath_ver}.gemspec
%{gem_dir}/specifications/default/csv-%{csv_ver}.gemspec
%{gem_dir}/specifications/default/date-%{date_ver}.gemspec
%{gem_dir}/specifications/default/dbm-%{dbm_ver}.gemspec
%{gem_dir}/specifications/default/e2mmap-%{e2mmap_ver}.gemspec
%{gem_dir}/specifications/default/etc-%{etc_ver}.gemspec
%{gem_dir}/specifications/default/fcntl-%{fcntl_ver}.gemspec
%{gem_dir}/specifications/default/fiddle-%{fiddle_ver}.gemspec
%{gem_dir}/specifications/default/fileutils-%{fileutils_ver}.gemspec
%{gem_dir}/specifications/default/forwardable-%{forwardable_ver}.gemspec
%{gem_dir}/specifications/default/gdbm-%{gdbm_ver}.gemspec
%{gem_dir}/specifications/default/ipaddr-%{ipaddr_ver}.gemspec
%{gem_dir}/specifications/default/logger-%{logger_ver}.gemspec
%{gem_dir}/specifications/default/matrix-%{matrix_ver}.gemspec
%{gem_dir}/specifications/default/mutex_m-%{mutex_m_ver}.gemspec
%{gem_dir}/specifications/default/ostruct-%{ostruct_ver}.gemspec
%{gem_dir}/specifications/default/openssl-%{openssl_ver}.gemspec
%{gem_dir}/specifications/default/prime-%{prime_ver}.gemspec
%{gem_dir}/specifications/default/rexml-%{rexml_ver}.gemspec
%{gem_dir}/specifications/default/rss-%{rss_ver}.gemspec
%{gem_dir}/specifications/default/scanf-%{scanf_ver}.gemspec
%{gem_dir}/specifications/default/sdbm-%{sdbm_ver}.gemspec
%{gem_dir}/specifications/default/shell-%{shell_ver}.gemspec
%{gem_dir}/specifications/default/stringio-%{stringio_ver}.gemspec
%{gem_dir}/specifications/default/strscan-%{strscan_ver}.gemspec
%{gem_dir}/specifications/default/sync-%{sync_ver}.gemspec
%{gem_dir}/specifications/default/thwait-%{thwait_ver}.gemspec
%{gem_dir}/specifications/default/tracer-%{tracer_ver}.gemspec
%{gem_dir}/specifications/default/webrick-%{webrick_ver}.gemspec
%{gem_dir}/specifications/default/zlib-%{zlib_ver}.gemspec

%{_mandir}/man1/erb%{ruby_suffix}.1*
%{_mandir}/man1/ri%{ruby_suffix}.1*

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%doc ruby_%{doc_version}_stdlib
%doc ruby_%{doc_version}_core

%files doc-ri
%defattr(644,root,root,755)
%{ruby_ridir}/ACL
%{ruby_ridir}/ARGF
%{ruby_ridir}/Abbrev
%{ruby_ridir}/Addrinfo
%{ruby_ridir}/ArgumentError
%{ruby_ridir}/Array
%{ruby_ridir}/Base64
%{ruby_ridir}/BasicObject
%{ruby_ridir}/BasicSocket
%{ruby_ridir}/Benchmark
%{ruby_ridir}/BigDecimal
%{ruby_ridir}/BigMath
%{ruby_ridir}/Binding
%{ruby_ridir}/Bundler
%{ruby_ridir}/CGI
%{ruby_ridir}/CMath
%{ruby_ridir}/CSV
%{ruby_ridir}/Class
%{ruby_ridir}/ClosedQueueError
%{ruby_ridir}/Comparable
%{ruby_ridir}/Complex
%{ruby_ridir}/ConditionVariable
%{ruby_ridir}/Continuation
%{ruby_ridir}/Coverage
%{ruby_ridir}/DBM
%{ruby_ridir}/DBMError
%{ruby_ridir}/DEBUGGER__
%{ruby_ridir}/DRb
%{ruby_ridir}/Data
%{ruby_ridir}/Date
%{ruby_ridir}/DateTime
%{ruby_ridir}/Delegator
%{ruby_ridir}/Digest
%{ruby_ridir}/Dir
%{ruby_ridir}/ENV
%{ruby_ridir}/EOFError
%{ruby_ridir}/ERB
%{ruby_ridir}/EXCEPTION_TYPE
%{ruby_ridir}/Encoding
%{ruby_ridir}/EncodingError
%{ruby_ridir}/English
%{ruby_ridir}/Enumerable
%{ruby_ridir}/Enumerator
%{ruby_ridir}/Errno
%{ruby_ridir}/Etc
%{ruby_ridir}/Exception
%{ruby_ridir}/Exception2MessageMapper
%{ruby_ridir}/FalseClass
%{ruby_ridir}/Fcntl
%{ruby_ridir}/Fiber
%{ruby_ridir}/FiberError
%{ruby_ridir}/Fiddle
%{ruby_ridir}/File
%{ruby_ridir}/FileTest
%{ruby_ridir}/FileUtils
%{ruby_ridir}/Find
%{ruby_ridir}/Float
%{ruby_ridir}/FloatDomainError
%{ruby_ridir}/Forwardable
%{ruby_ridir}/FrozenError
%{ruby_ridir}/GC
%{ruby_ridir}/GDBM
%{ruby_ridir}/GDBMError
%{ruby_ridir}/GDBMFatalError
%{ruby_ridir}/Gem
%{ruby_ridir}/GetoptLong
%{ruby_ridir}/HTTPClientException
%{ruby_ridir}/HTTPGatewayTimeOut
%{ruby_ridir}/HTTPMovedTemporarily
%{ruby_ridir}/HTTPMultipleChoice
%{ruby_ridir}/HTTPRequestEntityTooLarge
%{ruby_ridir}/HTTPRequestTimeOut
%{ruby_ridir}/HTTPRequestURITooLarge
%{ruby_ridir}/HTTPRequestURITooLong
%{ruby_ridir}/HTTPRequestedRangeNotSatisfiable
%{ruby_ridir}/Hash
%{ruby_ridir}/IO
%{ruby_ridir}/IOError
%{ruby_ridir}/IPAddr
%{ruby_ridir}/IPSocket
%{ruby_ridir}/IRB
%{ruby_ridir}/IndexError
%{ruby_ridir}/Integer
%{ruby_ridir}/Interrupt
%{ruby_ridir}/JSON
%{ruby_ridir}/Jacobian
%{ruby_ridir}/Kconv
%{ruby_ridir}/Kernel
%{ruby_ridir}/KeyError
%{ruby_ridir}/LUSolve
%{ruby_ridir}/LoadError
%{ruby_ridir}/LocalJumpError
%{ruby_ridir}/Logger
%{ruby_ridir}/MakeMakefile
%{ruby_ridir}/Marshal
%{ruby_ridir}/MatchData
%{ruby_ridir}/Math
%{ruby_ridir}/Matrix
%{ruby_ridir}/Method
%{ruby_ridir}/Module
%{ruby_ridir}/Monitor
%{ruby_ridir}/MonitorMixin
%{ruby_ridir}/Mutex
%{ruby_ridir}/Mutex_m
%{ruby_ridir}/NKF
%{ruby_ridir}/NameError
%{ruby_ridir}/Net
%{ruby_ridir}/Newton
%{ruby_ridir}/NilClass
%{ruby_ridir}/NoMemoryError
%{ruby_ridir}/NoMethodError
%{ruby_ridir}/NotImplementedError
%{ruby_ridir}/Numeric
%{ruby_ridir}/OLEProperty
%{ruby_ridir}/Object
%{ruby_ridir}/ObjectSpace
%{ruby_ridir}/Observable
%{ruby_ridir}/Open3
%{ruby_ridir}/OpenSSL
%{ruby_ridir}/OpenStruct
%{ruby_ridir}/OpenURI
%{ruby_ridir}/OptionParser
%{ruby_ridir}/PP
%{ruby_ridir}/PStore
%{ruby_ridir}/PTY
%{ruby_ridir}/Pathname
%{ruby_ridir}/PrettyPrint
%{ruby_ridir}/Prime
%{ruby_ridir}/Proc
%{ruby_ridir}/Process
%{ruby_ridir}/Profiler__
%{ruby_ridir}/Psych
%{ruby_ridir}/Queue
%{ruby_ridir}/RDoc
%{ruby_ridir}/RDocTask
%{ruby_ridir}/REXML
%{ruby_ridir}/RSS
%{ruby_ridir}/Racc
%{ruby_ridir}/Rake
%{ruby_ridir}/Random
%{ruby_ridir}/Range
%{ruby_ridir}/RangeError
%{ruby_ridir}/Rational
%{ruby_ridir}/RbConfig
%{ruby_ridir}/Readline
%{ruby_ridir}/Regexp
%{ruby_ridir}/RegexpError
%{ruby_ridir}/Resolv
%{ruby_ridir}/Rinda
%{ruby_ridir}/Ripper
%{ruby_ridir}/RubyLex
%{ruby_ridir}/RubyToken
%{ruby_ridir}/RubyVM
%{ruby_ridir}/RuntimeError
%{ruby_ridir}/SDBM
%{ruby_ridir}/SDBMError
%{ruby_ridir}/SOCKSSocket
%{ruby_ridir}/Scanf
%{ruby_ridir}/ScriptError
%{ruby_ridir}/SecureRandom
%{ruby_ridir}/SecurityError
%{ruby_ridir}/Set
%{ruby_ridir}/Shell
%{ruby_ridir}/Shellwords
%{ruby_ridir}/Signal
%{ruby_ridir}/SignalException
%{ruby_ridir}/SimpleDelegator
%{ruby_ridir}/SingleForwardable
%{ruby_ridir}/Singleton
%{ruby_ridir}/SizedQueue
%{ruby_ridir}/Socket
%{ruby_ridir}/SocketError
%{ruby_ridir}/SortedSet
%{ruby_ridir}/StandardError
%{ruby_ridir}/StopIteration
%{ruby_ridir}/String
%{ruby_ridir}/StringIO
%{ruby_ridir}/StringScanner
%{ruby_ridir}/Struct
%{ruby_ridir}/Symbol
%{ruby_ridir}/Sync
%{ruby_ridir}/Sync_m
%{ruby_ridir}/Synchronizer
%{ruby_ridir}/Synchronizer_m
%{ruby_ridir}/SyntaxError
%{ruby_ridir}/Syslog
%{ruby_ridir}/SystemCallError
%{ruby_ridir}/SystemExit
%{ruby_ridir}/SystemStackError
%{ruby_ridir}/TCPServer
%{ruby_ridir}/TCPSocket
%{ruby_ridir}/TSort
%{ruby_ridir}/TempIO
%{ruby_ridir}/Tempfile
%{ruby_ridir}/ThWait
%{ruby_ridir}/Thread
%{ruby_ridir}/ThreadError
%{ruby_ridir}/ThreadGroup
%{ruby_ridir}/ThreadsWait
%{ruby_ridir}/Time
%{ruby_ridir}/Timeout
%{ruby_ridir}/TracePoint
%{ruby_ridir}/Tracer
%{ruby_ridir}/TrueClass
%{ruby_ridir}/TypeError
%{ruby_ridir}/UDPSocket
%{ruby_ridir}/UNIXServer
%{ruby_ridir}/UNIXSocket
%{ruby_ridir}/URI
%{ruby_ridir}/UnboundMethod
%{ruby_ridir}/UncaughtThrowError
%{ruby_ridir}/UnicodeNormalize
%{ruby_ridir}/Vector
%{ruby_ridir}/WEBrick
%{ruby_ridir}/WIN32OLE
%{ruby_ridir}/WIN32OLERuntimeError
%{ruby_ridir}/WIN32OLEQueryInterfaceError
%{ruby_ridir}/WIN32OLE_EVENT
%{ruby_ridir}/WIN32OLE_METHOD
%{ruby_ridir}/WIN32OLE_PARAM
%{ruby_ridir}/WIN32OLE_RECORD
%{ruby_ridir}/WIN32OLE_TYPE
%{ruby_ridir}/WIN32OLE_TYPELIB
%{ruby_ridir}/WIN32OLE_VARIABLE
%{ruby_ridir}/WIN32OLE_VARIANT
%{ruby_ridir}/Warning
%{ruby_ridir}/WeakRef
%{ruby_ridir}/XML
%{ruby_ridir}/XMLEncoding_ja
%{ruby_ridir}/XMP
%{ruby_ridir}/YAML
%{ruby_ridir}/ZeroDivisionError
%{ruby_ridir}/Zlib
%{ruby_ridir}/fatal
%{ruby_ridir}/lib
%{ruby_ridir}/syntax
%{ruby_ridir}/page-CONTRIBUTING_md.ri
%{ruby_ridir}/page-COPYING.ri
%lang(ja) %{ruby_ridir}/page-COPYING_ja.ri
%{ruby_ridir}/page-LEGAL.ri
%{ruby_ridir}/page-NEWS*.ri
%{ruby_ridir}/page-README_md.ri
%lang(ja) %{ruby_ridir}/page-README_ja_md.ri
%{ruby_ridir}/page-*_rdoc.ri
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{oname}-%{pkg_version}
