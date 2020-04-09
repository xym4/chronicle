import time, os, requests

DB_API_URL = 'http://db-api-108704205.us-east-1.elb.amazonaws.com/alter'

# Set the filename and open the file
filename = 'chronicle.log'
file = open(filename,'r')

# Find the size of the file and move to the end
st_results = os.stat(filename)
st_size = st_results[6]
file.seek(st_size)

while True:
    where = file.tell()
    line = file.readline()
    if not line:
        time.sleep(1)
        file.seek(where)
    else:

        # looking for log line of format:
        # INFO:werkzeug:66.102.8.201 - - [09/Apr/2020 03:30:53] "^[[37mGET /static/img/square.gif?xym.yao@gmail.com_email_A_256880228643415940347055016340732801407 HTTP/1.1^[[0m" 200 -

        if 'GET /static/img/logo.gif?' in line:
            metadata_start_index = line.index('?') + 1
            metadata_end_index = line.index(' HTTP/1.1')
            message_id = line[metadata_start_index:metadata_end_index]
            metadata = message_id.split('_')
            print(metadata)

            contact, comm_type, campaign_id = metadata[0], metadata[1], metadata[2]

            update_data = {
                'contact': contact,
                'comm_type': comm_type,
                'campaign_id': campaign_id,
                'message_id': message_id
            }

            # update communications db is_read status to 'Y'
            resp = requests.put(DB_API_URL, json=update_data)
            print(str(resp))

