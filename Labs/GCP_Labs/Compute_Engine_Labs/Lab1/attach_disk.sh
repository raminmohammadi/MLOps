sudo mkfs.ext4 -F /dev/sdb
sudo mkdir /mlops-disk
sudo mount /dev/sdb /mlops-disk
sudo chown r.mohammadi /mlops-disk
scp -r Lab1/ r.mohammadi@35.226.100.89:/mlops_disk


# Machine 2
sudo mkdir /mlops-disk
sudo mount /dev/sdb /mlops-disk
