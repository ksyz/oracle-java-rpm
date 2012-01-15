%define section  non-free
%define priority 16030
%define javaver  1.6.0
%define origin   sun
%ifarch x86_64
%define sdklnk         java-%{javaver}-%{origin}.%{_arch}
%define jrelnk         jre-%{javaver}-%{origin}.%{_arch}
%else
%define sdklnk         java-%{javaver}-%{origin}
%define jrelnk         jre-%{javaver}-%{origin}
%endif

Name:           %{sdklnk}-jce-policy
Version:        %{javaver}
Release:        2jpp
Epoch:          0
Summary:        JCE unlimited strength jurisdiction policy files

Group:          Security/Cryptography
License:        Non-distributable, restricted use, see README.txt
Vendor:         JPackage Project
Distribution:   JPackage
URL:            http://java.sun.com/javase/
Source0:        jce_policy-6.zip
#NoSource:       0
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch

BuildRequires:  jpackage-utils >= 0:1.5.26
Requires:       java-%{javaver}-%{origin} >= 0:1.6.0

%description
Due to import control restrictions, the version of JCE policy files
that are bundled in the JDK(TM) 6 environment allow "strong" but
limited cryptography to be used.  This package provides "unlimited
strength" policy files which contain no restrictions on cryptographic
strengths.


%prep
%setup -q -n jce


%build
# Not.


%install
rm -rf $RPM_BUILD_ROOT
install -d -m 755 \
  $RPM_BUILD_ROOT%{_jvmprivdir}/%{sdklnk}/jce/unlimited
install -p -m 644 local_policy.jar US_export_policy.jar \
  $RPM_BUILD_ROOT%{_jvmprivdir}/%{sdklnk}/jce/unlimited


%clean
rm -rf $RPM_BUILD_ROOT


%post
update-alternatives \
  --install \
    %{_jvmdir}/%{jrelnk}/lib/security/local_policy.jar \
    jce_%{javaver}_%{origin}_local_policy \
    %{_jvmprivdir}/%{sdklnk}/jce/unlimited/local_policy.jar \
    %{priority} \
  --slave \
    %{_jvmdir}/%{jrelnk}/lib/security/US_export_policy.jar \
    jce_%{javaver}_%{origin}_us_export_policy \
    %{_jvmprivdir}/%{sdklnk}/jce/unlimited/US_export_policy.jar

%preun
if [ $1 -eq 0 ] ; then
  update-alternatives \
    --remove \
      jce_%{javaver}_%{origin}_local_policy \
      %{_jvmprivdir}/%{sdklnk}/jce/unlimited/local_policy.jar
fi


%files
%defattr(-,root,root,-)
%doc README.txt COPYRIGHT.html
%{_jvmprivdir}/*


%changelog
* Mon Jul 18 2011 Jiri Vanek <jvanek at redaht.com> - 0:1.6.0-2jpp
- intorduced variables sdklnk and jrelnk which corespond to sun java arch dependent naming conventions
-resolves rhbz#713200

* Mon Dec 11 2006 Ville Skyttä <scop at jpackage.org> - 0:1.6.0-1jpp
- 1.6.0.

* Wed Nov 22 2006 Ville Skyttä <scop at jpackage.org> - 0:1.6.0-0.1.rc.1jpp
- 1.6.0-rc, based on 1.5.0-1jpp.
