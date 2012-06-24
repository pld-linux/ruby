Summary:	Ruby - interpreted scripting language
Summary(ja):	���֥������Ȼظ�����Ruby���󥿥ץ꥿
Summary(pl):	Ruby - interpretowany j�zyk skryptowy
Summary(pt_BR): Linguagem de script orientada a objeto
Summary(zh_CN):	ruby - һ�ֿ��ٸ�Ч���������ű��������
Name:		ruby
Version:	1.6.7
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	ftp://ftp.ruby-lang.org/pub/ruby/%{name}-%{version}.tar.gz
Source1:	ftp://ftp.netlab.co.jp/pub/lang/ruby/doc/%{name}-texi-1.4-en.tar.gz
Source2:	http://www.math.sci.hokudai.ac.jp/~gotoken/ruby/%{name}-uguide-981227.tar.gz
Source3:	ftp://ftp.netlab.co.jp/pub/lang/ruby/doc/%{name}faq-990927.tar.gz
Source4:	irb.1
Patch0:		%{name}-info.patch
Patch1:		%{name}-ac25x.patch
URL:		http://www.ruby-lang.org/
BuildRequires:	autoconf
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel >= 4.2
BuildRequires:	texinfo
BuildRequires:	tk-devel
Requires(post,postun):/sbin/ldconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ruby-doc

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming. It has many features to process text
files and to do system management tasks (as in Perl). It is simple,
straight-forward, extensible, and portable.

%description -l ja
Ruby�ϥ���ץ뤫�Ķ��Ϥʥ��֥������Ȼظ�������ץȸ���Ǥ���Ruby�Ϻǽ�
������ʥ��֥������Ȼظ�����Ȥ����߷פ���Ƥ��ޤ����顤���֥�������
�ظ��ץ���ߥ󥰤��ڤ˹Ԥ���������ޤ����������̾�μ�³�����Υ�
����ߥ󥰤��ǽ�Ǥ���

Ruby�ϥƥ����Ƚ����ط���ǽ�Ϥʤɤ�ͥ�졤Perl��Ʊ�����餤���ϤǤ�������
�˥���ץ��ʸˡ�ȡ��㳰�����䥤�ƥ졼���ʤɤε����ˤ�äơ����ʬ����
�䤹���ץ���ߥ󥰤�����ޤ���

%description -l pl
Ruby to interpretowany j�zyk skryptowy, w sam raz dla �atwego i
szybkiego pisania zorientowanych obiektowo program�w. Ma wiele funkcji
u�atwiaj�cych przetwarzanie plik�w tekstowych i wykonywanie prac
zwi�zanych z zarz�dzaniem systemu (podobnie jak Perl). Jest prosty,
rozszerzalny i przeno�ny.

%description -l pt_BR
Ruby � uma linguagem de script interpretada de programa��o
orientada a objeto. Possui diversas caracter�sticas para
processamento de texto. � simples, extens�vel e direta.

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
