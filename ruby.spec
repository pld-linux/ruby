%define ruby_ridir %{_datadir}/ri/1.8/system
Summary:	Ruby - interpreted scripting language
Summary(ja):	オブジェクト指向言語Rubyインタプリタ
Summary(pl):	Ruby - interpretowany j�zyk skryptowy
Summary(pt_BR):	Linguagem de script orientada a objeto
Summary(zh_CN):	ruby - 匯嶽酔堀互丼議中�魘塹鷭撤庄牾毛鑵�
Name:		ruby
Version:	1.8.2
%define pre preview2
Release:	2
License:	The Ruby License
Group:		Development/Languages
#Source0:	http://www.ruby-lang.org/%{name}-%{version}.tar.gz
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/1.8/%{name}-%{version}-%{pre}.tar.gz
# Source0-md5:	f40dae2bd20fd41d681197f1229f25e0
Source1:	http://www.ibiblio.org/pub/languages/ruby/doc/%{name}-texi-1.4-en.tar.gz
# Source1-md5:	839fda4af52b5c5c6d21f879f7fc62bf
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/%{name}-uguide-981227.tar.gz
# Source2-md5:	24eadcd067278901da9ad70efb146b07
Source3:	http://www.ibiblio.org/pub/languages/ruby/doc/%{name}faq-990927.tar.gz
# Source3-md5:	634c25b14e19925d10af3720d72e8741
Source4:	irb.1
Source5:	http://www.geocities.jp/kosako1/oniguruma/archive/onigd20040724.tar.gz
# Source5-md5:	06db0cda42b9034807ee14e91e6246fe
Patch0:		%{name}-info.patch
Patch1:		%{name}-LIB_PREFIX.patch
Patch2:		%{name}-ia64.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	texinfo
BuildRequires:	tk-devel
Requires(post,postun):/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ruby-doc
Obsoletes:	rdoc
Obsoletes:	ruby-REXML

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
Rubyはシンプルかつ強力なオブジェクト指向スクリプト言語です．Rubyは最初
から純粋なオブジェクト指向言語として設計されていますから，オブジェクト
指向プログラミングを手軽に行う事が出来ます．もちろん通常の手続き型のプ
ログラミングも可能です．

Rubyはテキスト処理関係の能力などに優れ，Perlと同じくらい強力です．さら
にシンプルな文法と，例外処理やイテレータなどの機構によって，より分かり
やすいプログラミングが出来ます．

%description -l pl
Ruby to interpretowany j�zyk skryptowy, w sam raz dla �atwego i
szybkiego pisania zorientowanych obiektowo program�w. Ma wiele funkcji
u�atwiaj�cych przetwarzanie plik�w tekstowych i wykonywanie prac
zwi�zanych z zarz�dzaniem systemu (podobnie jak Perl). Jest prosty,
rozszerzalny i przeno�ny.

%description -l pt_BR
Ruby � uma linguagem de script interpretada de programa艫o
orientada a objeto. Possui diversas caracter�sticas para
processamento de texto. � simples, extens�vel e direta.

%package tk
Summary:	Ruby/Tk bindings
Summary(pl):	Wi�zania Ruby/Tk
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description tk
This pachage contains Ruby/Tk bindings.

%description tk -l pl
Ten pakiet zawiera wi�zania Ruby/Tk.

%package devel
Summary:	Ruby development libraries
Summary(pl):	Biblioteki programistyczne interpretera j�zyka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description devel
Ruby development libraries.

%description devel -l pl
Biblioteki programistyczne interpretera j�zyka Ruby.

%package static
Summary:	Ruby static libraries
Summary(pl):	Biblioteki statyczne Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description static
Ruby static libraries.

%description devel -l pl
Biblioteki statyczne Ruby.

%prep
%setup -q -a1 -a2 -a3 -a5
%patch0 -p1
%patch1 -p1
#%patch2 -p1

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
	--with-X11-lib=/usr/X11R6/%{_lib}
%{__make}

%{__make} info -C %{name}-texi-1.4-en

./miniruby -I lib bin/rdoc -o rdoc
./miniruby -I lib -I ext/syck bin/rdoc --ri -o ri

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

cp -a ri/ri/* $RPM_BUILD_ROOT%{ruby_ridir}

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
%doc guide faq misc README README.EXT ChangeLog ToDo rdoc
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
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/[a-s]*
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/[u-z]*
%dir %{_ulibdir}/%{name}/site_ruby
%dir %{_ulibdir}/%{name}/site_ruby/1.8
%dir %{_ulibdir}/%{name}/site_ruby/1.8/*-linux*
%dir %{ruby_ridir}
%{ruby_ridir}/*

%{_mandir}/*/*
%{_infodir}/*.info*
%{_examplesdir}/%{name}-%{version}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so

%files static
%{_libdir}/lib*.a

%files tk
%defattr(644,root,root,755)
%{_libdir}/%{name}/1.8/tcltk.rb
%{_libdir}/%{name}/1.8/tk*.rb
%{_libdir}/%{name}/1.8/tk
%{_libdir}/%{name}/1.8/tkextlib
%attr(755,root,root) %{_libdir}/%{name}/1.8/*-linux*/t*.so
