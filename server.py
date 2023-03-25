import firebase_admin
from firebase_admin import db , messaging
import networkx as nx
import random
import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km

    try:
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
    except Exception as e:
        print(e)
        print(lat1, lon1, lat2, lon2)

    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    a = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


database_url = "https://firstflutter-9b67d-default-rtdb.europe-west1.firebasedatabase.app"

cred_obj = firebase_admin.credentials.Certificate('./my_cred.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':database_url
	})


# ref2 = db.reference("/connections")
# ref2.set({
#         'hello' : 'rolds'
#     })



ref = db.reference("/locations")
fetch_data = ref.get()
users = list()
# print(fetch_data)
for id , user_position  in fetch_data.items():
    # print(id,user_position)
    users.append([id,float(user_position['latitude']),float(user_position['longitude']),])
    
# print(users)

graph = nx.Graph()


# Add nodes for each user
for user in users:
    graph.add_node(user[0])
# Add edges with weights as the difference between their values
for i in range(len(users)):
    for j in range(i+1, len(users)):
        weight = calculate_distance(users[i][1], users[i][2], users[j][1], users[i][2])
        graph.add_edge(users[i][0], users[j][0], weight=weight)

# Draw the graph
pos = nx.spring_layout(graph)  # layout nodes using the spring layout algorithm
nx.draw(graph, pos, with_labels=True)  # draw the graph with labels
labels = nx.get_edge_attributes(graph, 'weight')  # get the weight labels for edges
nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)  # draw weight labels for edges


print(labels)
#print(labels)

#--------------------------------------- PART 2 ---------------------------------------


connectionsLista = list()
for key, value in labels.items():
    if value < 0.5:
        print("111111111111111111111111111")
        print(key)
        connectionsLista.append(key)

ref2 = db.reference("/connections")
for pearson in connectionsLista:
    ref2.push().set({
        "atomo1" : pearson[0],
        "atomo2" : pearson[1],
    })



# Create a list containing up to 500 registration tokens.
# These registration tokens come from the client FCM SDKs.
registration_tokens = [
    'fJ5OX22uSFaEqMq58wXoQZ:APA91bHc3BI31pBaH2Pq2T2PqRJIEj8VggUD7fiBSI_5UfXQOqdvExdd9ywLuaQtrxDsxqPcs5ch61H1DBRavhGpX-qB9M5FuWgaqIw0bkbA_rtUtCI4nfavWpy24UFCbPhrZQmAad9n',
]

message = messaging.Message(
    data={'title': '850', 'body': '2:45'},
    token='fJ5OX22uSFaEqMq58wXoQZ:APA91bHc3BI31pBaH2Pq2T2PqRJIEj8VggUD7fiBSI_5UfXQOqdvExdd9ywLuaQtrxDsxqPcs5ch61H1DBRavhGpX-qB9M5FuWgaqIw0bkbA_rtUtCI4nfavWpy24UFCbPhrZQmAad9n',
)
response = messaging.send(message)
# See the BatchResponse reference documentation
# for the contents of response.
print('{0} messages were sent successfully'.format(response))