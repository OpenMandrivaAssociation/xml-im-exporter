# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1

%define section free

Summary:        XML Im-/Exporter
Name:           xml-im-exporter
Version:        1.1
Release:        %mkrel 2.0.10
Epoch:          0
License:        LGPL
URL:            http://xml-im-exporter.sourceforge.net/
Group:          Development/Java
Source0:        xml-im-exporter1.1.tgz
Source1:        xml-im-exporter-1.1.pom
Patch0:         xml-im-exporter-build_xml.patch
BuildRequires:  ant >= 0:1.6
BuildRequires:  ant-junit
BuildRequires:  java-rpmbuild >= 0:1.6
BuildRequires:  junit
%if %{gcj_support}
BuildRequires:    java-gcj-compat-devel
%else
BuildArch: noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
XML Im-/Exporter is a low level library to assist 
you in the straight forward process of importing 
and exporting XML from and to your Java classes. 
All of this is designed having performance and 
simplicity in mind.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}.

%prep
%setup -q -n %{name}
# XXX: file encoding invalid
%{__rm} src/test/de/zeigermann/xml/XMLWriterTest.java
# remove all binary libs
find . -name "*.jar" -exec rm -f {} \;
#for j in $(find . -name "*.jar"); do
#    mv $j $j.no
#done

%patch0 -b .sav

%{_bindir}/find . -type f -name '*.txt' -o -type f -name '*.html' -o -type f -name '*.css' -o -type f -name package-list | \
  %{_bindir}/xargs -t %{__perl} -pi -e 's/\r$//g'

%build
export CLASSPATH=$(build-classpath junit)
export OPT_JAR_LIST="ant/ant-junit"
%{ant} jar test javadocs


%install
rm -rf %{buildroot}

# jars
install -d -m 755 %{buildroot}%{_javadir}

install -m 644 build/lib/%{name}%{version}.jar \
  %{buildroot}%{_javadir}/%{name}-%{version}.jar
(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

#poms
%add_to_maven_depmap de.zeigermann.xml xml-im-exporter %{version} JPP/ xml-im-exporter
install -d -m 755 %{buildroot}%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    %{buildroot}%{_datadir}/maven2/poms/JPP-xml-im-exporter.pom
    
# javadoc
install -d -m 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr doc/javadoc/* %{buildroot}%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}


# docs
install -d -m 755 %{buildroot}%{_docdir}/%{name}-%{version}
install -m 644 doc/index.html %{buildroot}%{_docdir}/%{name}-%{version}
install -m 644 *.txt %{buildroot}%{_docdir}/%{name}-%{version}

%{__perl} -pi -e 's/\r$//g' %{buildroot}%{_docdir}/%{name}-%{version}/Copying.txt \
%{buildroot}%{_javadocdir}/%{name}-%{version}/**/**/**/*

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%post
%update_maven_depmap
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%{_datadir}/doc/%{name}-%{version}/index.html
%{_datadir}/doc/%{name}-%{version}/*.txt
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
