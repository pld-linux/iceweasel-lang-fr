%define		_lang		fr
Summary:	French resources for Iceweasel
Summary(pl.UTF-8):	Francuskie pliki językowe dla Iceweasela
Name:		iceweasel-lang-%{_lang}
Version:	3.0.9
Release:	1
License:	MPL 1.1 or GPL v2+ or LGPL v2.1+
Group:		I18n
Source0:	http://ftp.mozilla.org/pub/mozilla.org/firefox/releases/%{version}/linux-i686/xpi/%{_lang}.xpi
# Source0-md5:	7be481c1595300ec83ca0632a0e5fd8f
URL:		http://www.mozilla.org/
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
Requires:	iceweasel >= %{version}
Provides:	iceweasel-lang-resources = %{version}
Obsoletes:	mozilla-firefox-lang-fr
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_iceweaseldir	%{_datadir}/iceweasel
%define		_chromedir	%{_iceweaseldir}/chrome

%description
French resources for Iceweasel.

%description -l pl.UTF-8
Francuskie pliki językowe dla Iceweasela.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_chromedir},%{_iceweaseldir}/defaults/profile}

unzip %{SOURCE0} -d $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT%{_libdir}/chrome/* $RPM_BUILD_ROOT%{_chromedir}
sed -e 's@chrome/%{_lang}\.jar@%{_lang}.jar@' $RPM_BUILD_ROOT%{_libdir}/chrome.manifest \
	> $RPM_BUILD_ROOT%{_chromedir}/%{_lang}.manifest
mv -f $RPM_BUILD_ROOT%{_libdir}/*.rdf $RPM_BUILD_ROOT%{_iceweaseldir}/defaults/profile
# rebrand locale for iceweasel
cd $RPM_BUILD_ROOT%{_chromedir}
unzip fr.jar locale/branding/brand.dtd locale/branding/brand.properties \
	locale/browser/appstrings.properties locale/browser/aboutDialog.dtd
sed -i -e 's/Mozilla Firefox/Iceweasel/g; s/Firefox/Iceweasel/g;' \
	locale/branding/brand.dtd locale/branding/brand.properties
sed -i -e 's/Firefox/Iceweasel/g;' locale/browser/appstrings.properties
grep -e '\<ENTITY' locale/browser/aboutDialog.dtd \
	> locale/browser/aboutDialog.dtd.new
sed -i -e '/copyrightInfo/s/^\(.*\)\..*Firefox.*/\1\./g; s/\r//g; /copyrightInfo/s/$/" >/g;' \
	locale/browser/aboutDialog.dtd.new
mv -f locale/browser/aboutDialog.dtd.new locale/browser/aboutDialog.dtd
zip -0 fr.jar locale/branding/brand.dtd locale/branding/brand.properties \
	locale/browser/appstrings.properties locale/browser/aboutDialog.dtd
rm -f locale/branding/brand.dtd locale/branding/brand.properties \
	locale/browser/appstrings.properties locale/browser/aboutDialog.dtd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_chromedir}/%{_lang}.jar
%{_chromedir}/%{_lang}.manifest
# file conflict:
#%{_iceweaseldir}/defaults/profile/*.rdf
