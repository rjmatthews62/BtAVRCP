# BtAVRCP
Simple PyBluez project for Bluetooth AVRCP 

A simple example of a Bluetooth AVRCP session.

Implemented in Python3 with PyBluez

You will need to change the "addr" settings in code to point to a your own device. 

If the service search does not immediately find your device, check that your device is on and not already connected to another host, and that the host machine's bluetooth adapter is actually on.

Sometimes it takes a few attempts to connect.

AVRCP Spec: https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=309020

AVCTP Spec: https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=260858

Some things that I found confusing:

The AVRCP (Audio Visual Remote Control Protocol) runs on top of the AVCTP (AUDIO/VIDEO CONTROL
TRANSPORT PROTOCOL).

The three leading bytes are part of AVCTP.
<pre>
0: 7..4: Incrementing transaction id. 0x01 to 0x0f
   3..2: Packet type 00 = self contained packet
     1 : 0=request 1=response
     0 : 0=PID recognized 1: PID error
1-2: 2 byte bigendian profile id (in this case 110e, AVRCP)
</pre>
(ie, 10 11 0e)

All the specific AVRCP packets are tagged with the header (0x48,0x00,0x00,0x19,0x58)

This translates as:
<pre>
0x48 : Subunit spec (Type=9 (panel), Subunit id=0, encoded in bits 7..3 and 2..1 respectively)
0x00 : Opcode (always 0 for AVRCP specific packets)
0x001958: Is the BT SIG company identifier

The actual PDU byte follows the header.
</pre>
The other main packet type I have observed is opcode 0x7c, or Passthrough. 

I'm still not sure where the operation_ids are actually defined, but I found a workable list which is included in the body of the python code.

Example:
<pre>
Received on initial connection:
10 11 0e 01 48 00 00 19 58 10 00 00 01 03 
10 11 0e = AVCTP header.
01 = Command type STATUS
48 00 00 19 58 = AVRCP identifier
00 = reserved
10 = getCapabilities
00 01 = parameter length
03 = Get supported event list

When Play/Pause button is pressed:
20 11 0e 00 48 7c 44 00 
20 11 0e = AVCTP Header
00 = Command Type CONTROL
48 = Subunit iD (always 0x48 for AVRCP)
7c = Passthrough command
44 = Action (in this case PLAY. PAUSE=0x46. See operation_ids in code. These tend to toggle)
00 = Operation data length (in this case, none)
</pre>
