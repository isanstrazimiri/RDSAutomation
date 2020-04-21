import csv #File reading library
import boto3 #connects and talks to AWS
import db as db
from pwgen import pwgen #generates password for AWS


client= boto3.client('rds') #creates a client and will pass the service
'''
creates a new db dictionary with names : saas01, saas02..
they will be passed into the database'''
#Will be created 10 saas dbs since range is (10)
new_dbs  = {'saas{:0>2}'.format(db): '' for db in range(10)}
#Loop over the db dictionary all the keys(instance names)
for db in new_dbs.keys():
    new_dbs[db]=pwgen(20) #gen passwd
    client.create_db_cluster(
        AvailabilityZones=[
            "us-east-1b",
            "us-east-1b"
        ],
        BackupRetentionPeriod=1,
        DBClusterIdentifier=db,
        VpcSecurityGroupsIds=[
            'sg-0aa5e07ebdabfb0d1'
        ],
        DBSubnetGroupName="default-vpc-0f38b2e75ac4e6349",
        Enginer="aurora",
        MasterUsername="root",
        MasterUserPassword=new_dbs[db],
        StorageEncrypted=True,
        EngineMode="serverless",
        ScalingConfiguration={ 
            "MinCapacity": 2,
            "MaxCapacity": 64,
            "AutoPause": True,
            "SecondsUntilAutoPause": 300
        },
        DeletionProtection=True #Protects from deleting
    )
#We have to create a csv file to keep the databases
#Now we will open loop over the database and write the csv file

with open('newdbs.csv','w',newline='')as f:
    writer=csv.writer(f)
    [writer.writerow(db) for db in new_dbs.items()]
