# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "debian/jessie64"
  config.vm.synced_folder ".", "/movit", :mount_options => ["dmode=777","fmode=700"]
  config.vm.provision :shell, path: ".provision/bootstrap.sh"
  config.vm.network "private_network", ip: "10.0.3.69"
end

