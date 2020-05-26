# python-cloudswitch

cloud instance manager

```
Usage: cloudswitch
   [-U|--start]
   [-D|--stop]
   [-L|--list]
   [-r|--region] <region>
   [-t|--tag] <name:value>
   [-v|--verbose]
``` 

## start all stopped instances

```
cloudswitch -U
```

## stop all running instances

```
cloudswitch -D
```

## start by tag

```
cloudswitch -U -t tagname:tagvalue
```

Multiple tags:

```
cloudswitch -U -t postgres:master -t postgres:replica
```

## start by region

```
cloudswitch -U -r eu-north-1
```

Multiple regions are also accepted:

```
cloudswitch -U -r eu-north-1 -r eu-south-1 -r eu-picamoixons-3
```

## list instances on a particular region

```
cloudswitch -L -r eu-west-1
```

## list instances using a particular tag

```
cloudswitch -L -r postgres:master
```