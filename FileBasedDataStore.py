import threading
import time
import argparse
import json
import sys
from threading import*

def initialise(x): #it initialises the directory path if file not present it create the json file
    global directory
    directory = x
    try:
        with open(directory,'r') as openfile:
            data = json.load(openfile)
    except:
        f = open(directory, "w")
        f.write("{}")
        f.close()

def create(key,value,timeout=0):
    with open(directory,'r') as openfile:
        data = json.load(openfile)
    if key in data:  #check if the key to insert is already present
            print("\nError: This key already exists")
    else:
        if(key.isalpha()):
            if sys.getsizeof(data)<(1024*1024*1024) and sys.getsizeof(value)<= (16*1024): #checks for file size less than 1GB and Jason object value less than 16KB 
                if timeout == 0:  
                        val=[value,time.time()+30] #initialise the time-to-live for values if none given it automatically assigns 30secs
                else:
                        val=[value,time.time()+timeout] #adding user defined timeout to the value
                if len(key)<=32: #checks for input key_name capped at 32chars
                        data[key] = val
                else:
                    print("\nError: Key limit exceeded!! ")
            else:
                print("\nError: Memory limit exceeded!! ")
        else:
                print("\nError: Invalid Key!! Key must contain only alphabets and no special characters or numbers")
        with open(directory,'w') as openfile:
            json.dump(data,openfile,indent=4)

def read(key):
    with open(directory,'r') as openfile:
        data = json.load(openfile)
    if key not in data: #checks if the key is present or not
        print("\nError: given key does not exist in database. Please enter a valid key")
    else:
        b=data[key]
        if time.time() < b[1]: #comparing the present time with expiry time
            stri="{"+'\"'+key+'\"'+":"+'\"'+str(b[0])+'\"'+"}" #to return the value in the format of JasonObject i.e.,"key_name:value"
            return stri
        else:
            print("\nError: time-to-live of ",key," has expired")

def delete(key):
    with open(directory,'r') as openfile:
        data = json.load(openfile)
    if key not in data: #checks key is present or not
        print("\nError: Given key does not exist in database. Please enter a valid key")
    else:
        b=data[key]
        if time.time() < b[1]: #comparing the current time with expiry time
            del data[key]
            with open(directory,'w') as openfile:
                data = json.dump(data,openfile,indent=4)
            print("\nThe Key ",key," is successfully deleted")
        else:
            print("\nError: time-to-live of ",key," has expired")

def parse_args():
    parser = argparse.ArgumentParser(description='Generates arguments')
    parser.add_argument("--directory",
                        dest="directory",
                        required=False,
                        help="Directory Path for the JSON file")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    directory = args.directory
    if directory is None:
        directory = "data.json"
    initialise(directory)

#Statements to run directly from main file with threading
    print("\n-----------------File Based Data Store with CRD support-----------------\n ")
    option = int(input("\n1.Create\n2.Read\n3.Delete\n"))
    if(option == 1):
        key = input("\nEnter Key Value (String Only)")
        value = input("\nEnter Value for the Key")
        timeout = int(input("\nEnter the time-to-live value (Integer)"))
        #create(key,value,timeout)
        t1 = threading.Thread(target=create,args=(key,value,timeout)) #threading
        t1.start()
        time.sleep(2)
    elif(option == 2):
        key = input("\nEnter Key value for reading the vlaue")
        #result = read(key)
        #print(result)
        t2 = threading.Thread(target=read,args=(key)) #threading
        t2.start()
        time.sleep(3)
    elif(option == 3):
        key = input("\nEnter the value to delete the key value pair")
        #delete(key)
        t3 = threading.Thread(target=delete,args=(key,value,timeout)) #threading
        t3.start()
        time.sleep(4)
    else:
        print("\nError : Select options from 1 to 3")

