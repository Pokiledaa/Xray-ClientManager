curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

python3 get-pip.py

pip install image qrcode psutil requests python-docx

python3 setup.py

# Here we Copy and Setup our stricker watcher
cp /root/Xray-ClientManager/systemd/xray-mgmt.service  /etc/systemd/system
systemctl daemon-reload
systemctl enable xray-mgmt.service
systemctl start xray-mgmt.service
