## Pre-requisites
- Router and computerhave to be connected over LAN. 
- Modbus TCP must be enabled
- Your computer needs to have ruby and modbus-cli installed. 
To do so type these commands in terminal:
```
sudo apt-get install ruby
```
```
sudo gem install modbus-cli
```

## How to use


## Configuration
- A configuration file is formatted as json file
- Configuration file must be named **config.json**
- For every device, there are a few things that **must** be defined in order for automated tests to work
  - Device name
  - Authentication parameters
    - Modbus Port
    - SSH IP address
    - SSH Port
    - SSH Username
    - SSH Password
  - List of commands
     - Modbus register number
     - Number of modbus registers
     - SSH equivalent command
