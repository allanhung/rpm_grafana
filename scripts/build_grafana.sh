export RPMBUILDROOT=/root/rpmbuild
export GOPATH=/usr/share/gocode

# go repo
rpm --import https://mirror.go-repo.io/centos/RPM-GPG-KEY-GO-REPO
curl -s https://mirror.go-repo.io/centos/go-repo.repo | tee /etc/yum.repos.d/go-repo.repo
# epel
yum install -y epel-release
# work around for nodejs
rpm -ivh https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm
yum -y install nodejs golang git bzip2 rpm-build
mkdir -p $RPMBUILDROOT/SOURCES && mkdir -p $RPMBUILDROOT/SPECS && mkdir -p $RPMBUILDROOT/SRPMS
# fix rpm marcos
sed -i -e "s#.centos##g" /etc/rpm/macros.dist

# get grafana
go get github.com/grafana/grafana
rm -rf $GOPATH/src/github.com/grafana/grafana

export GRAFANAVER=4.5.0-beta1
cd $GOPATH/src/github.com/grafana
git clone --depth=10 -b v$GRAFANAVER https://github.com/grafana/grafana.git


# build backend
cd grafana
go run build.go build

# build frontend
npm install -g yarn
NODEVER=`node --version`
NPMVER=`npm --version`
sed -i -e "s/\"node\":.*/\"node\": \"${NODEVER:1:10}\",/g" -e "s/\"npm\":.*/\"npm\": \"${NPMVER}\"/g" package.json
yarn install --pure-lockfile
npm run build

rpmbuild -bb $RPMBUILDROOT/SPECS/grafana.spec
