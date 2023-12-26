# sync-tool

This tool synchronizes keyboards and mouses on multiple PCs.
For example, you can move multiple characters at the same time in multiple game accounts.
This tool uses LAN (Local Area Network) for communication.

There were not any sync tools for keyboards and mouse for Windows PC. So I created this tool for Windows and other OS. This tool can be downloaded from my github.

However, some Android emulators have sync tools.
* Bluestacks - Multi-Instance Sync: https://www.bluestacks.com/features/multi-instance-sync.html
* LDPlayer - Synchronizer Tool: https://www.ldplayer.net/blog/introduction-to-synchronizer.html

## Introduction video for Windows 64bit
https://youtu.be/ZoZgP2ll-s0

## Install for Windows 64bit
1. Download the two exe files (sync-server.exe, sync-client.exe) from this github to each PC.
2. Run "sync-server.exe" on server PC
3. Select the "Allow access" button when the "Windows Security Alert" window appears.
4. Run "client_client.exe" on each client PC
5. Input the IP address of the server PC to the client PC.
6. To turn sync on/off, press Ctrl-F2 on the server PC.

## Install for other OS
1. Download python3.10 from https://www.python.org/
2. Install python3.10 on each PC
3. Install pynput module. "pip install pynput" on each PC
4. Download the two exe files (sync-server.py, sync-client.py) from this github to each PC.
5. Run "sync-server.py" on server PC
6. Open port 65432/tcp on server PC
7. Run "sync-client.py" on each client PC
8. Input the IP address of the server PC to the each client PC.
9. To turn sync on/off, press Ctrl-F2 on the server PC.

## Troubleshooting
* Server and client cannot communicate. In that case, please check the firewall settings on the server PC. For example, on Windows 10, open "Windows Defender Firewall" -> "Allow an app or feature through Windows Defender Firewall" and allow "sync-server.exe".

## Notes
* Communication content is not encrypted.
* This tool is open source software. In other words, it is free software whose source code can be freely modified and redistributed.
* I will not be held responsible if any scandal occurs to you.




