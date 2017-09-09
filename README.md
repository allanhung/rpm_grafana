RPMBUILD for grafana
=========================

Grafana rpm

How to Build
=========
    git clone https://github.com/allanhung/rpm_grafana
    cd rpm_grafana
    docker run --name=grafana_build --rm -ti -v $(pwd)/rpms:/root/rpmbuild/RPMS -v $(pwd)/specs/grafana.spec:/root/rpmbuild/SPECS/grafana.spec -v $(pwd)/scripts:/usr/local/src/build centos /bin/bash -c "/usr/local/src/build/build_grafana.sh"

# check
    docker run --name=grafana_check --rm -ti -v $(pwd)/rpms:/root/rpmbuild/RPMS centos /bin/bash -c "yum localinstall -y /root/rpmbuild/RPMS/x86_64/grafana-*.rpm"
