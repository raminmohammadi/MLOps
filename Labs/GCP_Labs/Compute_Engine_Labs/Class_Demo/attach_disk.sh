sudo mkfs.ext4 -F /dev/sdb
sudo mkdir /mlops-disk
sudo mount /dev/sdb /mlops-disk
sudo chown <YOUR EMAIL> /mlops-disk
scp -r Lab1/ <YOUR EMAIL>@<IP TO THE MACHINE>:/mlops_disk


# Machine 2
sudo mkdir /mlops-disk
sudo mount /dev/sdb /mlops-disk
