import pickle
mylist=[]
with open('chat_history.pkl', 'wb') as f:
    pickle.dump(mylist, f)
with open('chat_history.pkl', 'rb') as f:
    mynewlist = pickle.load(f)
print(mynewlist)
