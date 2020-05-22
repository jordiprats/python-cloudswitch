from __future__ import print_function

import sys
import boto3
import getopt

def eprint(*args, **kwargs):
    #print(*args, file=sys.stderr, **kwargs)

def showJelp(msg):
    print("Usage: "+sys.argv[0])
    print("   [-U|--start]")
    print("   [-D|--stop]")
    print("   [-L|--list]")
    print("   [-r|--region] <region>")
    print("   [-t|--tag] <name:value>")
    print("   [-v|--verbose]")
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
    verbose = False

    # parse opts
    try:
        options, remainder = getopt.getopt(sys.argv[1:], 'UDLt:r:vh', [
                                                                    'start',
                                                                    "stop",
                                                                    "list",
                                                                    "tag",
                                                                    "region",
                                                                    "verbose",
                                                                    'help'
                                                                 ])
    except Exception, e:
        showJelp(str(e))

    for opt, arg in options:
        if opt in ('-U', '--start'):
            action = 'start'
        elif opt in ('-D', '--stop'):
            action = 'stop'
        elif opt in ('-L', '--list'):
            action = 'list'
        elif opt in ('-t', '--tag'):
            try:
                instance_filtering = True
                filter = {}
                filter['Name'] = 'tag:'+arg.split(':')[0]
                filter['Values'] = [ arg.split(':')[1] ]

                instance_filter.append(filter)
            except Exception as e:
                showJelp("invalid tag: "+arg+' ('+str(e)+')')
        elif opt in ('-r', '--region'):
            regions.append(arg)
            custom_regionset = True
        elif opt in ('-v', '--verbose'):
            verbose = True
        else:
            showJelp("")

    if action == 'noop':
        showJelp("noop")

    if not custom_regionset:
        regions = getRegions()
    
    if verbose:
        eprint('regions: '+str(regions))
        eprint('filter: '+str(instance_filter))

    for region in regions:
        if verbose:
            eprint("== "+region+" ==")
        ec2 = boto3.client('ec2',region_name=region)
        if instance_filtering:
            response = ec2.describe_instances(Filters=instance_filter)
        else:
            response = ec2.describe_instances()
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                if verbose:
                    eprint(instance['PublicDnsName']+' '+instance['State']['Name']+' ACTION: '+action)
                if action == 'stop':
                    if instance['State']['Name'] == 'running':
                        stopInstance(instance["InstanceId"])
                elif action == 'start':
                    if instance['State']['Name'] == 'stopped':
                        startInstance(instance["InstanceId"])
                elif action == 'list':
                    print(instance['PublicDnsName']+': '+instance['State']['Name'])
                else:
                    showJelp(action+' is NOT currently implemented')
