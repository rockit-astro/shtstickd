## Shtstick internal temperature/humidity sensor daemon

`shtstickd` wraps a [shtstick](https://github.com/rockit-astro/shtstick) sensor and
makes the latest measurement available for other services via Pyro.

`shtstick` is a commandline utility that reports the latest weather data.

### Configuration

Configuration is read from json files that are installed by default to `/etc/shtstickd`.
A configuration file is specified when launching the server, and the `shtstick` frontend will search this location when launched.

```python
{
  "daemon": "localhost_test", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "shtstickd", # The name to use when writing messages to the observatory log.
  "control_machines": ["LocalHost"], # Machine names that are allowed to control (rather than just query) state. Machine names are registered in `rockit.common.IP`.
  "serial_port": "/dev/ttyACM0", # Serial FIFO for communicating with the vaisala
  "serial_baud": 115200, # Serial baud rate
  "serial_timeout": 5, # Serial comms timeout
}
```

The FIFO device names are defined in the .rules files installed through the `rockit-shtstick-data-*` rpm packages.
If the physical serial port or USB adaptors change these should be updated to match.

### Initial Installation

The automated packaging scripts will push 5 RPM packages to the observatory package repository:

| Package                      | Description                                                               |
|------------------------------|---------------------------------------------------------------------------|
| rockit-shtstick-server       | Contains the `shtstickd` server and systemd service file.                 |
| rockit-shtstick-client       | Contains the `shtstick` commandline utility for controlling the server.   |
| rockit-shtstick-data-warwick | Contains the json configuration and udev rules for The Marsh Observatory. |
| python3-rockit-shtstick      | Contains the python module with shared code.                              |

Alternatively, perform a local installation using `sudo make install`.

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now shtstickd@<config>
```

where `config` is the name of the json file for the appropriate unit.

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the shtstick config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart shtstickd@<config>
```

### Testing Locally

The server and client can be run directly from a git clone:
```
./shtstickd ./config/test.json
SHTSTICKD_CONFIG_PATH=./config/test.json ./shtstick status
```
