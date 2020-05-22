# python-cloudswitch

cloud instance manager

```
Usage: cloudswitch
   [-U|--start]
   [-D|--stop]
   [-r|--region]
   [-t|--tag] <name:value>
``` 

## start all stopped instances

```
python cloudswitch.py -U
```

## stop all running instances

```
python cloudswitch.py -D
```

## start by tag

```
python cloudswitch.py -U -t tagname:tagvalue
```

Multiple tags:

```
python cloudswitch.py -U -t postgres:master -t postgres:replica
```

## start by region

```
python cloudswitch.py -U -r eu-north-1
```

Multiple regions are also accepted:

```
python cloudswitch.py -U -r eu-north-1 -r eu-south-1 -r eu-picamoixons-3
```