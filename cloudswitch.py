import sys
import boto3
import getopt

def showJelp(msg):
    print("Usage: "+sys.argv[0])
    print("   [-U|--start]")
    print("   [-D|--stop]")
    print("   [-r|--region]")
    print("   [-t|--tag] <name:value>")
    print("")
    sys.exit(msg)

def stopInstance(instance_id):
    if not isinstance(instance_id, list):
        instante_id_array = [ instance_id ]
    else:
        instante_id_array = instance_id
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=instante_id_array).stop()

def startInstance(instance_id):
    if not isinstance(instance_id, list):
        instante_id_array = [ instance_id ]
    else:
        instante_id_array = instance_id
    ec2 = boto3.resource('ec2')
    ec2.instances.filter(InstanceIds=instante_id_array).start()

def getRegions():
    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
    return regions

if __name__ == "__main__":

    action = 'noop'
    instance_filtering = False
    regions = []
    custom_regionset = False
    instance_filter = []

    # parse opts
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'UDt:r:h', [
                                                                    'start',
                                                                    "stop",
                                                                    "tag",
                                                                    "region",
                                                                    'help'
                                                                 ])
    except Exception, e:
        showJelp(str(e))

    for opt, arg in options:
        if opt in ('-U', '--start'):
            action = 'start'
        elif opt in ('-D', '--stop'):
            action = 'stop'
        elif opt in ('-t', '--tag'):
            try:
                instance_filtering = True
                filter = {}
                filter['Name'] = 'tag:'+arg.split(':')[0]
                filter['Values'] = arg.split(':')[1]

                instance_filter.append(filter)
            except Exception as e:
                showJelp("invalid tag: "+arg+' ('+str(e)+')')
        elif opt in ('-r', '--region'):
            regions.append(arg)
            custom_regionset = True
        else:
            showJelp("")

    if action == 'noop':
        showJelp("noop")

    if not custom_regionset:
        regions = getRegions()
    
    for region in regions:
        print("== "+region+" ==")
        ec2 = boto3.client('ec2',region_name=region)
        if instance_filtering:
            response = ec2.describe_instances(instance_filter)
        else:
            response = ec2.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if action == 'stop':
                    if instance['State']['Name'] == 'running':
                        stopInstance(instance["InstanceId"])
                elif action == 'start':
                    if instance['State']['Name'] == 'stopped':
                        startInstance(instance["InstanceId"])
                else:
                    showJelp(action+' is NOT currently implemented')
