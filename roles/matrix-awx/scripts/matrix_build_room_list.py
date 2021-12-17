
import sys
import requests
import json

janitor_token = sys.argv[1]
synapse_container_ip = sys.argv[2]
synapse_container_port = sys.argv[3]

# collect total amount of rooms

rooms_raw_url = 'http://' + synapse_container_ip + ':' + synapse_container_port + '/_synapse/admin/v1/rooms'
rooms_raw_header = {'Authorization': 'Bearer ' + janitor_token}
rooms_raw = requests.get(rooms_raw_url, headers=rooms_raw_header)
rooms_raw_python = json.loads(rooms_raw.text)
total_rooms = rooms_raw_python["total_rooms"]

# build complete room list file

room_list_file = open("/tmp/room_list_complete.json", "w")

for i in range(0, total_rooms, 100):
  rooms_inc_url = 'http://' + synapse_container_ip + ':' + synapse_container_port + '/_synapse/admin/v1/rooms?from=' + str(i)
  rooms_inc = requests.get(rooms_inc_url, headers=rooms_raw_header)
  room_list_file.write(rooms_inc.text)

room_list_file.close()

print(total_rooms)
