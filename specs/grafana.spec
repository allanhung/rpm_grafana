%global debug_package   %{nil}
%global provider        github
%global provider_tld    com
%global project         grafana
%global repo            grafana
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}
%global _version        4.5.0-beta1
%global commit          bc690232fb893c5d2798b501f3e847771650be07
%global shortcommit     %(c=%{commit}; echo ${c:0:7})
%global gopath          %{_datadir}/gocode

Name:           grafana
Version:        4.5.0_beta1
Release:        1.git%{shortcommit}%{?dist}
Summary:      	Grafana is an open source, feature rich metrics dashboard and graph editor
License:        BSD
URL:            https://%{import_path}
Source0:        grafana-grafana-%{_version}.tar.gz
Requires:       expect
Requires:       fontconfig
Requires:       freetype
Requires:       urw-fonts


%description
Grafana is an open source, feature rich metrics dashboard and graph editor for Graphite, Elasticsearch, OpenTSDB, Prometheus and InfluxDB.


%prep


%build


%install
install -D -p -m 0755 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/bin/%{repo}-cli %{buildroot}%{_sbindir}/%{repo}-cli
install -D -p -m 0755 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/bin/%{repo}-server %{buildroot}%{_sbindir}/%{repo}-server
install -d -m 0755 %{buildroot}%{_datadir}/%{repo}/conf
cp -a $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/conf/* %{buildroot}%{_datadir}/%{repo}/conf/
install -d -m 0755 %{buildroot}%{_datadir}/%{repo}/public
cp -a $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/public_gen/* %{buildroot}%{_datadir}/%{repo}/public/
install -d -m 0755 %{buildroot}%{_datadir}/%{repo}/scripts
cp -a $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/scripts/* %{buildroot}%{_datadir}/%{repo}/scripts/
install -d -m 0755 %{buildroot}%{_datadir}/%{repo}/vendor/phantomjs
install -D -p -m 0644 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/vendor/phantomjs/render.js %{buildroot}%{_datadir}/%{repo}/vendor/phantomjs/render.js
install -D -p -m 0755 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/vendor/phantomjs/phantomjs %{buildroot}%{_datadir}/%{repo}/vendor/phantomjs/phantomjs
install -d -m 0755  %{buildroot}%{_sysconfdir}/%{repo}
install -D -p -m 0644 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/conf/sample.ini %{buildroot}%{_sysconfdir}/%{repo}/grafana.ini
install -D -p -m 0644 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/conf/ldap.toml %{buildroot}%{_sysconfdir}/%{repo}/ldap.toml
install -d -m 0755  %{buildroot}%{_sysconfdir}/sysconfig
install -D -p -m 0644 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/packaging/rpm/sysconfig/grafana-server %{buildroot}%{_sysconfdir}/sysconfig/grafana-server
install -d -m 0755  %{buildroot}%{_unitdir}
install -D -p -m 0644 $GOPATH/src/%{provider}.%{provider_tld}/%{project}/%{repo}/packaging/rpm/systemd/grafana-server.service %{buildroot}%{_unitdir}/grafana-server.service
install -d -m 0755  %{buildroot}%{_var}/log/grafana
install -d -m 0755  %{buildroot}%{_var}/lib/grafana


%check
# empty for now

%pre
getent group grafana >/dev/null || groupadd -r grafana
getent passwd grafana >/dev/null || useradd -r -g grafana -d %{_var}/lib/grafana -s /sbin/nologin -c "Grafana Dashboard" grafana
exit 0

%post
%systemd_post grafana-server
# Set user permissions on /var/log/grafana, /var/lib/grafana
chown -R grafana:grafana /var/log/grafana /var/lib/grafana
# configuration files should not be modifiable by grafana user, as this can be a security issue
chown -Rh root:grafana /etc/grafana/*
find /etc/grafana -type f -exec chmod 640 {} ';'
find /etc/grafana -type d -exec chmod 755 {} ';'


%preun
%systemd_preun grafana-server

%postun
%systemd_postun_with_restart grafana-server

%files
%{_sbindir}/%{repo}-cli
%{_sbindir}/%{repo}-server
%{_datadir}/%{repo}/conf
%{_datadir}/%{repo}/public
%{_datadir}/%{repo}/scripts
%{_datadir}/%{repo}/vendor/phantomjs/phantomjs
%{_datadir}/%{repo}/vendor/phantomjs/render.js
%{_var}/log/grafana
%{_var}/lib/grafana
%config(noreplace) %{_sysconfdir}/%{repo}/grafana.ini
%config(noreplace) %{_sysconfdir}/%{repo}/ldap.toml
%config(noreplace) %{_sysconfdir}/sysconfig/grafana-server
%{_unitdir}/grafana-server.service


%changelog
* Sat Sep 09 2017 root - 4.5.0_beta1
 - first version
