# SITAMOTO

Sitamoto is a Python Projects for dealing with your Home Automation.

## Requirements
- Raspberry Pi with Raspbian Buster installed.
- Python 2.7 or above with pip installed
- mongodb
- rng-tools
- hostapd
- dns-masq

## Installation
Prepare the Projects

```bash
cd
git clone https://gitlab.vascomm.co.id/iot_ceria/sita_device_socket.git sitamoto
cd sitamoto
cp config.ini.example config.ini
sudo python -m pip install -r requirements.txt
```

Craft the Database

```bash
cd database
python dbcreate.py
python dbretrieve.py
cd ..
```

## Usage
Setup launcher to autorun at startup

```bash
crontab -e

# at the end of file, add this code
@reboot sh /home/pi/sitamoto/launcher.sh > /home/pi/sitamoto/logs/logcronlog 2>&1
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
