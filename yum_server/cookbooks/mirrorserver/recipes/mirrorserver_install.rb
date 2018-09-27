bash 'mirrorserver_install' do
  user 'root'
  code <<-EOH
  yum install -y createrepo
  yum install -y yum-plugin-downloadonly
  yum install -y https://centos7.iuscommunity.org/ius-release.rpm
  yum install --downloadonly --downloaddir=/var/repo epel-release
  yum install --downloadonly --downloaddir=/var/repo python36u
  yum install --downloadonly --downloaddir=/var/repo python36u-pip
  yum install --downloadonly --downloaddir=/var/repo wget
  createrepo /var/repo/
  ln -s /var/repo /var/www/html/repo
  yum -y install policycoreutils-python
  semanage fcontext -a -t httpd_sys_content_t "/var/repo(/.*)?" && restorecon -rv /var/repo
  EOH
end
