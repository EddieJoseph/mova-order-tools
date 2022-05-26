import sys

def get_orders_path():
    #print('Number of arguments:', len(sys.argv), 'arguments.')
    #print('Argument List:', str(sys.argv[1]))
    if(len(sys.argv)<2):
        print("no input file found. define input file as first argument")
        sys.exit(-1)
    print("order input file: ",sys.argv[1])
    return sys.argv[1]

def get_groups_path():
    if(len(sys.argv)<3):
        print("no input file found. define input file as second argument")
        sys.exit(-1)
    print("groups input file: ", sys.argv[2])
    return sys.argv[2]