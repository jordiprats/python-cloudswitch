import sys
import boto3
import getopt

def showJelp(msg):
    print("Usage: "+sys.argv[0])
    print("   [-U|--start]")
    print("   [-D|--stop]")
    print("")
    sys.exit(msg)

def stopInstance(instance_id):
    if not isinstance(instance_id, list):
        instante_id_array = [ instance_id ]
    else:
        instante_id_array = instance_id
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=instante_id_array).stop()

def getRegions():
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return regions

if __name__ == "__main__":

    action = 'noop'

    # parse opts
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'UDh', [
                                                                    'start',
                                                                    "stop"
                                                                    'help'
                                                                 ])
    except Exception, e:
        showJelp(str(e))

    for opt, arg in options:
        if opt in ('-U', '--start'):
            action = 'start'
        elif opt in ('-D', '--stop'):
            action = 'stop'
        else:
            showJelp("")

    if action == 'noop':
        showJelp("noop")

    regions = getRegions()

    if action == 'stop':
        for region in regions:
            print("== "+region+" ==")
            ec2 = boto3.client('ec2',region_name=region)
            response = ec2.describe_instances()
            for reservation in response["Reservations"]:
                for instance in reservation["Instances"]:
                    if instance['State']['Name'] == 'running':
                        stopInstance(instance["InstanceId"])
#    elif action == 'start':
    else:
        showJelp(action+' is NOT currently implemented')
