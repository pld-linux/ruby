Summary:	Ruby - interpreted scripting language
Summary:	Ruby - interpretowany jêzyk skryptowy
Name:		ruby
Version:	1.6.3
Release:	2
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/Jêzyki
URL:		http://www.ruby-lang.org
Source0:	ftp://ftp.netlab.co.jp/pub/lang/ruby/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.netlab.co.jp/pub/lang/ruby/doc/%{name}-texi-1.4-en.tar.gz
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/%{name}-uguide-981227.tar.gz
Source3:	ftp://ftp.netlab.co.jp/pub/lang/ruby/doc/%{name}faq-990927.tar.gz
Patch0:		%{name}-info.patch
Patch1:		%{name}-readline.patch
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	texinfo
BuildRequires:	tk-devel
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text
files and to do system management tasks (as in Perl). It is simple,
straight-forward, extensible, and portable.

%description -l pl
Ruby to interpretowany jêzyk skryptowy, w sam raz dla ³atwego i
szybkiego pisania zorientowanych obiektowo programów. Ma wiele funkcji
u³atwiaj±cych przetwarzanie plików tekstowych i wykonywanie prac
zwi±zanych z zarz±dzaniem systemu (podobnie jak Perl). Jest prosty,
rozszerzalny i przeno¶ny.

%prep
%setup -q -T -b 0
%setup -q -T -D -a 1
%setup -q -T -D -a 2
%setup -q -T -D -a 3
%patch0 -p1
%patch1 -p1

%build
%configure \
	--enable-shared
%{__make}
%{__make} -C ruby-texi-1.4-en

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_examplesdir}/%{name}-%{version}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install %{name}-texi-1.4-en/ruby.info* $RPM_BUILD_ROOT%{_infodir}
mv -f ruby-uguide guide
mv -f rubyfaq faq

gzip -9nf README README.EXT ChangeLog ToDo

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
%doc guide faq misc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/%{name}
%{_infodir}/*
%{_examplesdir}/%{name}-%{version}

%{_mandir}/*/*
