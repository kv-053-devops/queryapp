Name:           query
Version:        1.0
Release:        0.2
Summary:        Trading app query part 

Group:          query_app
BuildArch:      noarch
License:        GPL
URL:            https://github.com/c4n2012/python_hw/tree/flask_app/query_app
Source0:        query-1.0.tar.gz

%description
Trading app query microservice

%global	username queryapp

%pre
getent group %{username} >/dev/null || groupadd -r %{username}
getent passwd %{username} >/dev/null || \
useradd -r -g %{username} -M -s /sbin/nologin \
-c "Account to own and run %{username}" %{username}
exit

%post
/usr/bin/systemctl start %{username}.service >/dev/null 2>&1 && \
/usr/bin/systemctl enable %{username}.service >/dev/null 2>&1

%preun
/usr/bin/systemctl stop %{username}.service >/dev/null 2>&1 && \
/usr/bin/systemctl disable %{username}.service >/dev/null 2>&1

%postun
getent passwd %{username} >/dev/null && userdel -r %{username} >/dev/null 2>&1

%prep

%setup -q -c

%build
%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
install -m 0755 -d $RPM_BUILD_ROOT/opt/%{username}
install -m 0755 -d $RPM_BUILD_ROOT/etc/systemd/system
install -m 0755 -d $RPM_BUILD_ROOT/etc/default
install -m 0750 flask_query_api.py $RPM_BUILD_ROOT/opt/%{username}/flask_query_api.py
install -m 0750 query_class.py $RPM_BUILD_ROOT/opt/%{username}/query_class.py
install -m 0750 requirements.txt $RPM_BUILD_ROOT/opt/%{username}/requirements.txt
install -m 0644 %{username}.service $RPM_BUILD_ROOT/etc/systemd/system/%{username}.service
install -m 0644 %{username} $RPM_BUILD_ROOT/etc/default/%{username}

%files
%defattr(0750, %{username}, %{username}, 0755)
/opt/%{username}
/opt/%{username}/flask_query_api.py
%attr(0644,root,root) /etc/systemd/system/%{username}.service

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%changelog
* Jul 17 2019 Stazzz  1.0.2.0
 - RPM release v.1.0.2
