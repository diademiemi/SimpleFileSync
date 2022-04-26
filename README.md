# SimpleFileSync
Simple Python program to sync a file to other hosts over an encrypted connection in a network on file modification

## Purpose
This program syncs one or more (text) files over an encrypted connection. It was made out of the need to synchronize a single configuration file from a cluster of servers. This configuration file could change from any of these servers, but had to stay in sync. We were surprised at the lack of programs that could easily do this without getting into an infinite loop or using a lot of resources.

## Functionality
Files are synced upon a modification to them using AES encryption with a shared secret to every host defined in the config file. 

## Configuration
| Variable| Description |
|---|---|
| `bind_ip` | IP to bind the socket to |
| `port` | Port to bind to and use for remote connections |
| `remote_hosts` | Lists of remote hosts to send files to and accept files from |
| `shared_secret` | 32 byte shared secret for all hosts used for encryption. **Must be the same across all hosts** |
| `synced_files` | Lists of files to sync and send from this host |


<details><summary>See default config file</summary><p>

## sync.yaml
```yaml
bind_ip: 0.0.0.0
port: 54321
remote_hosts:
- 10.10.10.1
- 10.10.10.2
shared_secret: 
synced_files:
- /home/user/test.txt
```
</p></details>

## Example
The following configuration was used to sync the `/home/vagrant/test.txt` file.
Goes without saying.. don't use this shared secret....

<details open><summary>Server 1 config</summary><p>

```yaml
bind_ip: 0.0.0.0
port: 54321
remote_hosts:
- 192.168.50.12
- 192.168.50.13
shared_secret: eBae19F3cd508242cd1CEFBaCCccd9D3
synced_files:
- /home/vagrant/test.txt
```
</p></details>

<details><summary>Server 2 config</summary><p>

```yaml
bind_ip: 0.0.0.0
port: 54321
remote_hosts:
- 192.168.50.11
- 192.168.50.13
shared_secret: eBae19F3cd508242cd1CEFBaCCccd9D3
synced_files:
- /home/vagrant/test.txt
```
</p></details>

<details><summary>Server 3 config</summary><p>

```yaml
bind_ip: 0.0.0.0
port: 54321
remote_hosts:
- 192.168.50.11
- 192.168.50.12
shared_secret: eBae19F3cd508242cd1CEFBaCCccd9D3
synced_files:
- /home/vagrant/test.txt
```
</p></details>

This is the log of going from the servers 1 through 3 and appending "Test from server #" to the file. Once one server appends their test message, it will immediately add it to the other servers too. At the end the file looks like:
```
Test from server 1
Test from server 2
Test from server 3
```
The file has synced successfully and is the same on every host!

<details open><summary>From server 1</summary><p>

```
Modified file /home/vagrant/test.txt
Sent new /home/vagrant/test.txt to 192.168.50.12
Sent new /home/vagrant/test.txt to 192.168.50.13
Received new /home/vagrant/test.txt from 192.168.50.12
Received new /home/vagrant/test.txt from 192.168.50.13
```
</p></details>

<details><summary>From server 2</summary><p>

```
Received new /home/vagrant/test.txt from 192.168.50.11
Modified file /home/vagrant/test.txt
Sent new /home/vagrant/test.txt to 192.168.50.11
Sent new /home/vagrant/test.txt to 192.168.50.13
Received new /home/vagrant/test.txt from 192.168.50.13
```
</p></details>

<details><summary>From server 3</summary><p>

```
Received new /home/vagrant/test.txt from 192.168.50.11
Received new /home/vagrant/test.txt from 192.168.50.12
Modified file /home/vagrant/test.txt
Sent new /home/vagrant/test.txt to 192.168.50.11
Sent new /home/vagrant/test.txt to 192.168.50.12
```
</p></details>
