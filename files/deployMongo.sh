#!/bin/bash
sudo yum -y update
echo "[MongoDB]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
gpgcheck=0
enabled=1" | sudo tee -a /etc/yum.repos.d/mongodb.repo

sudo yum install -y mongodb-org-server mongodb-org-shell mongodb-org-tools
sudo mkdir /data /log /journal
sudo mkfs.ext4 /dev/xvdh
sudo mkfs.ext4 /dev/xvdi
sudo mkfs.ext4 /dev/xvdj

echo '/dev/xvdh /data ext4 defaults,auto,noatime,noexec 0 0
/dev/xvdi /journal ext4 defaults,auto,noatime,noexec 0 0
/dev/xvdj /log ext4 defaults,auto,noatime,noexec 0 0' | sudo tee -a /etc/fstab

sudo mount /data
sudo mount /journal
sudo mount /log

sudo chown mongod:mongod /data /journal /log
sudo ln -s /journal /data/journal

echo '* soft nofile 64000
* hard nofile 64000
* soft nproc 32000
* hard nproc 32000' | sudo tee -a /etc/security/limits.conf

echo '* soft nproc 32000
* hard nproc 32000' | sudo tee -a /etc/security/limits.d/90-nproc.conf


sudo blockdev --setra 32 /dev/xvdh
sudo blockdev --setra 32 /dev/xvdi
sudo blockdev --setra 32 /dev/xvdj

echo 'ACTION=="add", KERNEL=="xvdh", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules
echo 'ACTION=="add", KERNEL=="xvdi", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules
echo 'ACTION=="add", KERNEL=="xvdj", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules

echo 300 | sudo tee /proc/sys/net/ipv4/tcp_keepalive_time
