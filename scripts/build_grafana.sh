export RPMBUILDROOT=/root/rpmbuild
export GOPATH=/usr/share/gocode

# go repo
rpm --import https://mirror.go-repo.io/centos/RPM-GPG-KEY-GO-REPO
curl -s https://mirror.go-repo.io/centos/go-repo.repo | tee /etc/yum.repos.d/go-repo.repo
# epel
yum install -y epel-release
# work around for nodejs
rpm -ivh https://kojipkgs.fedoraproject.org//packages/http-parser/2.7.1/3.el7/x86_64/http-parser-2.7.1-3.el7.x86_64.rpm
yum -y install nodejs golang git

# get grafana
go get github.com/grafana/grafana
cd $GOPATH/src/github.com/grafana/grafana

# build backend
go run build.go build

# build frontend
npm install -g yarn
NODEVER=`node --version`
NPMVER=`npm --version`
sed -i -e "s/\"node\":.*/\"node\": \"${NODEVER:1:10}\",/g" -e "s/\"npm\":.*/\"npm\": \"${NPMVER}\"/g" package.json
yarn install --pure-lockfile
npm run build
