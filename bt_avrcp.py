import bluetooth
import logging
import threading
import struct

L2CAP_UUID = "0100"
AVRCP_UUID = 0x110e
BTSIG_ID = 0x1958 # BT Sig company ID
AVRCP_HEADER = bytes((0x48,0x00,0x00,0x19,0x58)) # AVRCP specific commands header.

AVRCP_OPERATION_ID_CHANNEL_UP = 0x30
AVRCP_OPERATION_ID_CHANNEL_DOWN = 0x31
AVRCP_OPERATION_ID_SELECT = 0x00
AVRCP_OPERATION_ID_UP = 0x01
AVRCP_OPERATION_ID_DOWN = 0x02
AVRCP_OPERATION_ID_LEFT = 0x03
AVRCP_OPERATION_ID_RIGHT = 0x04
AVRCP_OPERATION_ID_ROOT_MENU = 0x09

AVRCP_OPERATION_ID_SKIP = 0x3C
AVRCP_OPERATION_ID_VOLUME_UP = 0x41
AVRCP_OPERATION_ID_VOLUME_DOWN = 0x42
AVRCP_OPERATION_ID_MUTE = 0x43

AVRCP_OPERATION_ID_PLAY = 0x44
AVRCP_OPERATION_ID_STOP = 0x45
AVRCP_OPERATION_ID_PAUSE = 0x46
AVRCP_OPERATION_ID_REWIND = 0x48
AVRCP_OPERATION_ID_FAST_FORWARD = 0x49
AVRCP_OPERATION_ID_FORWARD = 0x4B
AVRCP_OPERATION_ID_BACKWARD = 0x4C
AVRCP_OPERATION_ID_UNDEFINED = 0xFF

operation_ids={}
operation_ids[AVRCP_OPERATION_ID_CHANNEL_UP]="CHANNEL_UP"
operation_ids[AVRCP_OPERATION_ID_CHANNEL_DOWN]="CHANNEL_DOWN"
operation_ids[AVRCP_OPERATION_ID_SELECT]="SELECT"
operation_ids[AVRCP_OPERATION_ID_UP]="UP"
operation_ids[AVRCP_OPERATION_ID_DOWN]="DOWN"
operation_ids[AVRCP_OPERATION_ID_LEFT]="LEFT"
operation_ids[AVRCP_OPERATION_ID_RIGHT]="RIGHT"
operation_ids[AVRCP_OPERATION_ID_ROOT_MENU]="ROOT_MENU"
operation_ids[AVRCP_OPERATION_ID_SKIP]="SKIP"
operation_ids[AVRCP_OPERATION_ID_VOLUME_UP]="VOLUME_UP"
operation_ids[AVRCP_OPERATION_ID_VOLUME_DOWN]="VOLUME_DOWN"
operation_ids[AVRCP_OPERATION_ID_MUTE]="MUTE"
operation_ids[AVRCP_OPERATION_ID_PLAY]="PLAY"
operation_ids[AVRCP_OPERATION_ID_STOP]="STOP"
operation_ids[AVRCP_OPERATION_ID_PAUSE]="PAUSE"
operation_ids[AVRCP_OPERATION_ID_REWIND]="REWIND"
operation_ids[AVRCP_OPERATION_ID_FAST_FORWARD]="FAST_FORWARD"
operation_ids[AVRCP_OPERATION_ID_FORWARD]="FORWARD"
operation_ids[AVRCP_OPERATION_ID_BACKWARD]="BACKWARD"
operation_ids[AVRCP_OPERATION_ID_UNDEFINED]="UNDEFINED"

AVRCP_CTYPE_CONTROL = 0
AVRCP_CTYPE_STATUS = 1
AVRCP_CTYPE_SPECIFIC_INQUIRY =2
AVRCP_CTYPE_NOTIFY=3
AVRCP_CTYPE_GENERAL_INQUIRY=4
AVRCP_CTYPE_RESPONSE_NOT_IMPLEMENTED = 8
AVRCP_CTYPE_RESPONSE_ACCEPTED=9
AVRCP_CTYPE_RESPONSE_REJECTED=0xA
AVRCP_CTYPE_RESPONSE_IN_TRANSITION=0xb
AVRCP_CTYPE_RESPONSE_IMPLEMENTED=0xc
AVRCP_CTYPE_RESPONSE_CHANGED=0xd
AVRCP_CTYPE_RESPONSE_RESERVED=0xe
AVRCP_CTYPE_RESPONSE_INTERIM=0xf
command_types={}
command_types[AVRCP_CTYPE_CONTROL ]="CONTROL "
command_types[AVRCP_CTYPE_STATUS ]="STATUS "
command_types[AVRCP_CTYPE_SPECIFIC_INQUIRY ]="SPECIFIC_INQUIRY "
command_types[AVRCP_CTYPE_NOTIFY]="NOTIFY"
command_types[AVRCP_CTYPE_GENERAL_INQUIRY]="GENERAL_INQUIRY"
command_types[AVRCP_CTYPE_RESPONSE_NOT_IMPLEMENTED ]="RESPONSE_NOT_IMPLEMENTED "
command_types[AVRCP_CTYPE_RESPONSE_ACCEPTED]="RESPONSE_ACCEPTED"
command_types[AVRCP_CTYPE_RESPONSE_REJECTED]="RESPONSE_REJECTED"
command_types[AVRCP_CTYPE_RESPONSE_IN_TRANSITION]="RESPONSE_IN_TRANSITION"
command_types[AVRCP_CTYPE_RESPONSE_IMPLEMENTED]="RESPONSE_IMPLEMENTED"
command_types[AVRCP_CTYPE_RESPONSE_CHANGED]="RESPONSE_CHANGED"
command_types[AVRCP_CTYPE_RESPONSE_RESERVED]="RESPONSE_RESERVED"
command_types[AVRCP_CTYPE_RESPONSE_INTERIM]="RESPONSE_INTERIM"

AVRCP_NOTIFICATION_EVENT_PLAYBACK_STATUS_CHANGED = 0x01            # Change in playback status of the current track.
AVRCP_NOTIFICATION_EVENT_TRACK_CHANGED = 0x02                      # Change of current track
AVRCP_NOTIFICATION_EVENT_TRACK_REACHED_END = 0x03                  # Reached end of a track
AVRCP_NOTIFICATION_EVENT_TRACK_REACHED_START = 0x04                # Reached start of a track
AVRCP_NOTIFICATION_EVENT_PLAYBACK_POS_CHANGED = 0x05               # Change in playback position. Returned after the specified playback notification change notification interval
AVRCP_NOTIFICATION_EVENT_BATT_STATUS_CHANGED = 0x06                # Change in battery status
AVRCP_NOTIFICATION_EVENT_SYSTEM_STATUS_CHANGED = 0x07              # Change in system status
AVRCP_NOTIFICATION_EVENT_PLAYER_APPLICATION_SETTING_CHANGED = 0x08 # Change in player application setting
AVRCP_NOTIFICATION_EVENT_NOW_PLAYING_CONTENT_CHANGED = 0x09        # The content of the Now Playing list has changed, see 6.9.5.
AVRCP_NOTIFICATION_EVENT_AVAILABLE_PLAYERS_CHANGED = 0x0a          # The available players have changed, see 6.9.4.
AVRCP_NOTIFICATION_EVENT_ADDRESSED_PLAYER_CHANGED = 0x0b           # The Addressed Player has been changed, see 6.9.2.
AVRCP_NOTIFICATION_EVENT_UIDS_CHANGED = 0x0c                       # The UIDs have changed, see 6.10.3.3.
AVRCP_NOTIFICATION_EVENT_VOLUME_CHANGED = 0x0d                     # The volume has been changed locally on the TG see 6.13.3.
event_ids={}
event_ids[AVRCP_NOTIFICATION_EVENT_PLAYBACK_STATUS_CHANGED]="PLAYBACK_STATUS_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_TRACK_CHANGED]="TRACK_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_TRACK_REACHED_END]="TRACK_REACHED_END"
event_ids[AVRCP_NOTIFICATION_EVENT_TRACK_REACHED_START]="TRACK_REACHED_START"
event_ids[AVRCP_NOTIFICATION_EVENT_PLAYBACK_POS_CHANGED]="PLAYBACK_POS_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_BATT_STATUS_CHANGED]="BATT_STATUS_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_SYSTEM_STATUS_CHANGED]="SYSTEM_STATUS_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_PLAYER_APPLICATION_SETTING_CHANGED]="PLAYER_APPLICATION_SETTING_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_NOW_PLAYING_CONTENT_CHANGED]="NOW_PLAYING_CONTENT_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_AVAILABLE_PLAYERS_CHANGED]="AVAILABLE_PLAYERS_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_ADDRESSED_PLAYER_CHANGED]="ADDRESSED_PLAYER_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_UIDS_CHANGED]="UIDS_CHANGED"
event_ids[AVRCP_NOTIFICATION_EVENT_VOLUME_CHANGED]="VOLUME_CHANGED"


sequence = 0
playback_status=0

def getstr(s):
   try:
       s=s.decode("utf-8")
   except:
       pass
   return s 

def list_service_detail(addr):
    # discovery channel
    port=-1
    services = bluetooth.find_service(address=addr, uuid=L2CAP_UUID)
    search=("%04x" % AVRCP_UUID)
    for svc in services:
        logging.info("Service="+str(svc))
        for c in svc["service-classes"]:
            service_class = getstr(c).lower() 
            logging.info("Service class="+str(service_class))
#            print("Detail: "+service_class)
            if (service_class==search):
                port=svc['port'];
                print("Found avrcp.");
                print("Port="+str(port))
    return port

def unpack3(packet):
   result=0
   for i in range(3):
      result=(result<<8) | packet[i]
   return result

def parsebytes(data):
   result=""
   for b in data:
      result+="%02x " % b
   return result

def pack3(value):
   result=bytearray(3)
   for i in range(3):
      result[i]=(value>>(8*(2-i))) & 0xff
   return bytes(result)
                 
def parseevents(payload):
   result=""
   global playback_status
   i=0
   while (i<len(payload)):
      eventid=payload[i];
      if (eventid>0):
         eventval=struct.unpack(">I",payload[i+1:i+5])[0]
         if eventid==AVRCP_NOTIFICATION_EVENT_PLAYBACK_STATUS_CHANGED:
            playback_status=payload[i+1] # Playback status is 1 byte
         result+="Event %02x %s %d " % (eventid,event_ids.get(eventid,"?"),eventval)
      i+=5
   return result                       

def parseeventlist(payload):
   result=""
   for id in payload:
      result+="%02x %s " % (id,event_ids.get(id,"?"))
   return result

def parse_avrcp(packet):
   "Main handler of avrcp packets"
   
   global playback_status
   # AVCTP packet header
   ptype,pid=struct.unpack(">BH",packet[0:3])
   transactionlabel=(ptype >> 4)
   packet_type=(ptype >> 2) & 0x03
   cr=(ptype>>1) & 0x01
   ipid=(ptype & 0x01)
   print("Packet: label=%d type=%d c/r=%d ipid=%d %4x" % (transactionlabel,packet_type,cr,ipid,pid))
   try:
      ctype,subunit,pdu = struct.unpack(">BBB",packet[3:6])
   except:
      print("Invalid packet")
      return
   ctype=ctype & 0xf # Command type
   subunit_type = subunit >> 3 # For AVRCP, subunit is always 0x48
   subunit_id = subunit & 0x7;
   print("Ctype=%02x (%s) pdu=%02x" % (ctype,command_types.get(ctype,"?"),pdu))
   if (pdu==0x7c): # Passthrough is actually an AVCTP command.
      action=packet[6]
      arglen=packet[7]
      print("Operation="+operation_ids[action]+" Arglen="+str(arglen))
      if (action==AVRCP_OPERATION_ID_PLAY):
         playback_status=0x01
      elif (action==AVRCP_OPERATION_ID_PAUSE):
         playback_status=0x02
         
   elif (packet[4:9]==AVRCP_HEADER): # All AVRCP commands have a PDU of 0x00, followed by the BTSIG_ID as company id
      pdu_ops=packet[9] # Actual AVRCP command
      arglen=struct.unpack(">H",packet[11:13])[0]
      if (arglen>0):
         payload=payload=packet[13:13+arglen]
      else:
         payload=bytes()
      if (pdu_ops==0x10): # Get Capability.
         capabilityid=payload[0] # Can be 0x03 (supported events, or 0x02 Get Company IDs supported
         print("Get capability pdu=%02x capability id=%02x args=%d" % (pdu_ops,capabilityid,arglen))
         if (capabilityid==3):
            print("Eventids supported: "+parseeventlist(payload[1:]))
            if (cr==0): #Request
               respondsupportedevents(transactionlabel)
      elif (pdu_ops==0x31): #Register notification
         print("Register events: "+parseevents(payload))
         if (ctype==AVRCP_CTYPE_NOTIFY):
             respondevent(transactionlabel,payload)

def nextseq():
   global sequence
   sequence += 0x1
   if (sequence>0xf):
      sequence=0x1
   return sequence

def responsepacket(seq):
   "Construct AVCTP response header"
   b1=((seq & 0x0f) << 4) | 0x02 # Single packet, valid response
   return struct.pack(">BH",b1,AVRCP_UUID) # AVRCP PID

def requestpacket(seq):
   "Construct AVCTP request header"
   b1=((seq & 0x0f) << 4) | 0x00 # Single packet, request
   return struct.pack(">BH",b1,AVRCP_UUID) # AVRCP PID

def respondevent(seq,payload):
   "Respond to a 0x31 Register Event notification."
   global socket

   packet=responsepacket(seq)
   packet+=bytes((AVRCP_CTYPE_RESPONSE_CHANGED,)) 
   packet+=AVRCP_HEADER
   packet+=bytes((0x31,0x00)) # 0x31 = Register Event
   if (payload[0]==AVRCP_NOTIFICATION_EVENT_PLAYBACK_STATUS_CHANGED):
      # 0x00 Stopped, 0x01 Playing 0x02 paused 0x03 fwd_seek 0x04 rev_seek 0xff error
      payload=bytes((AVRCP_NOTIFICATION_EVENT_SYSTEM_STATUS_CHANGED,0x02)) 
   packet+=struct.pack(">H",len(payload)) # At present just echoing the setting back.
   packet+=payload
   socket.send(packet)
   print("sent ",parsebytes(packet))

def requesteventvolume():
   "Request to be notified of volume changes. Not current working..."
   seq=nextseq()
   packet=requestpacket(seq)
   packet+=bytes((AVRCP_CTYPE_NOTIFY,)) 
   packet+=AVRCP_HEADER
   packet+=bytes((0x31,0x00)) # 0x31 = Register Event
   payload=bytes((AVRCP_NOTIFICATION_EVENT_VOLUME_CHANGED,0x7f)) # 0x7f max volume.
   packet+=struct.pack(">H",len(payload)) 
   packet+=payload # PAram len.
   socket.send(packet)
   print("sent request",parsebytes(packet))
   
def respondsupportedevents(seq):
   "Respond to 0x10 GetCapabilities event"
   events=bytes((AVRCP_NOTIFICATION_EVENT_PLAYBACK_STATUS_CHANGED,AVRCP_NOTIFICATION_EVENT_VOLUME_CHANGED))
   eventlist=bytes((len(events),))+events # Include number of events.
   # print("Eventlist="+parsebytes(eventlist))
   #eventlist=bytes() # By reporting "No events supported", allows simpler passthrough functions.
   data=bytes((0x03,))+eventlist # 0x03 = Event capabilities. 
   b=constructstatusreq(True,seq,0x10,data)
   print("Respond to capability request "+parsebytes(b))
   socket.send(b)
   
               
def constructstatusreq(reply,seq,pdu,data):
   if reply:
      b=responsepacket(seq)
      ctype=AVRCP_CTYPE_RESPONSE_IMPLEMENTED
   else:
      b=requestpacket(seq)
      ctype=AVRCP_CTYPE_STATUS
   b+=bytes((ctype,)) # Status,
   b+=AVRCP_HEADER
   b+=struct.pack(">BB",pdu,0x00) # PDU ID, 0x00=reserved
   b+=struct.pack(">H",len(data)) # Param length
   if len(data)>0:
      b+=data
   return b

def sendcapabilityreq(socket):
   "Query remote device for event capabilites"
   seq=nextseq()
   data=bytes((0x03,)) # 0x03 = request events.
   b=constructstatusreq(False,seq,0x10,data) # 0x10 = get capabilities
   print("Writing..."+parsebytes(b))
   socket.send(b)
   
print("Searching for services.")
logging.basicConfig(level=logging.WARN, format='%(message)s')
# Change the address to your own device.
addr="e2:8b:8e:89:6c:07"  #S530 white
#addr="b2:eb:98:de:11:88" # BTS-06
#addr="00:0d:44:ee:d3:97" # X100 Yellow
port=list_service_detail(addr);
if (port>0):
    print("Attempting to connect to L2CAP port ",port)
    socket=bluetooth.BluetoothSocket(bluetooth.L2CAP);
    socket.connect((addr,port))
    print("Connected.")
    sendcapabilityreq(socket)
    while True:
      print("Waiting on read:")
      data=socket.recv(1024)
      #        print(data)
      s=""
      for b in data:
         s+= ("%02x" % b)+" "
      print(s)
      parse_avrcp(data)
      print("Status: Playback=%d" % (playback_status))
    socket.close()
                          
