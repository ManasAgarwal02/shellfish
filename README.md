# shellfish
This script gives full access of the client/target device to a host.
  * Contains custom build shell known as shellfish.
  * Uses reverse-shell multithreading to get the connection of client/target device.

## How to Use?
### client.py file:
The client.py file is meant to run on client/target device, thus it is recommended to use a server which has static IP address else the script will be of no use once the IP of target gets changed.
* Enter your(server) IP address in the "host" variable.

### shellfish - custom shell commands:
* `list-conn` - gives the list of all active clients/target name along with the select id.
* `select #id` - to connect the desired client/target device, change "#id" with the respective id number.
* `quit` - To close the connection.


### Important :
* This script by default prints hosts activity with the client's device on both host as well as client's terminal.
* To prevent printing on target's device just comment out or delete the line number 23 ie.. `print(str_out)` from client.py file.
