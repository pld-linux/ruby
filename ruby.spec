Summary:	Ruby - interpreted scripting language
Summary(pl):	Ruby - interpretowany jêzyk skryptowy
Name:		ruby
Version:	1.6.7
Release:	2
License:	GPL
Group:		Development/Languages
URL:		http://www.ruby-lang.org
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/%{name}-%{version}.tar.gz
# Source0-md5:	4213d723911ce346717d60256fa925e1
Source1:	ftp://ftp.netlab.co.jp/pub/lang/ruby/doc/%{name}-texi-1.4-en.tar.gz
# Source1-md5:	839fda4af52b5c5c6d21f879f7fc62bf
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/%{name}-uguide-981227.tar.gz
# Source2-md5:	24eadcd067278901da9ad70efb146b07
Source3:	ftp://ftp.netlab.co.jp/pub/lang/ruby/doc/%{name}faq-990927.tar.gz
# Source3-md5:	634c25b14e19925d10af3720d72e8741
Source4:	irb.1
Patch0:		%{name}-info.patch
Patch1:		%{name}-ac25x.patch
BuildRequires:	autoconf
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	texinfo
BuildRequires:	tk-devel
Prereq:		/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ruby-doc

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
%setup -q -a1 -a2 -a3
%patch0 -p1
%patch1 -p1

%build
%{__autoconf}
%configure \
	--enable-shared
%{__make}

%{__make} info -C %{name}-texi-1.4-en

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_mandir}/man1,%{_examplesdir}/%{name}-%{version}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install sample/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
install %{name}-texi-1.4-en/ruby.info* $RPM_BUILD_ROOT%{_infodir}
install %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man1

mv -f ruby-uguide guide
mv -f rubyfaq faq

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
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/%{name}
%{_mandir}/*/*
%{_infodir}/*
%{_examplesdir}/%{name}-%{version}
