import boto3
import pandas as pd
import json
path_to_json = 'cred.json'

with open(path_to_json, 'r') as f:
    keys = json.load(f)
# Fetch Instances along with their attributes using Describe Instance Types and filter them out
def ec2_instance_types(region_name):
    ec2 = boto3.client('ec2', region_name=region_name, aws_access_key_id=keys['aws_access_key_id'], aws_secret_access_key=keys['aws_secret_access_key'])
    print('Start EC2 instance types Method')
    resultlist = []
    describe_result = ec2.describe_instance_types( InstanceTypes=['t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge', 'm4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge', 'm4.10xlarge', 'm4.16xlarge'])

    for i in describe_result['InstanceTypes']:
        result = {}
        memory = i['MemoryInfo']['SizeInMiB']/1024

        result['Offering']=i['InstanceType']
        result['vCPU']=i['VCpuInfo']['DefaultVCpus']
        result['Memory']=memory
        result['Storage']= 'EBS-only'
        result['Network Performance']=i['NetworkInfo']['NetworkPerformance']
        if 'EbsOptimizedInfo' in i['EbsInfo']:
            result['Dedicated EBS Bandwidth (Mbps)']=i['EbsInfo']['EbsOptimizedInfo']['BaselineBandwidthInMbps']
       
        resultlist.append(result)
        # print('resultlist' ,resultlist)
    return resultlist


# Create a list of EC2 Instance Types along with their configuration information For EPC
def ec2_offerings_setup(region_name):
    ec2 = boto3.client('ec2', region_name=region_name, aws_access_key_id='AKIA5HMXIFKSOP6NZ6YB', aws_secret_access_key='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')
    print('Start EC2 offerings setup Method')
    resultlist = []
    
    describe_result = ec2.describe_instance_types( InstanceTypes=['t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge', 'm4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge', 'm4.10xlarge', 'm4.16xlarge'])

    for i in describe_result['InstanceTypes']:
        result = {}
        result['Offering Name']=i['InstanceType']
        result['Offering Code']="CRMA_" + "_".join(i['InstanceType'].upper().split('.'))
        result['Description']=''
        result['Object Type']=''
        result['Specification Type']='Product'
        result['Orderable']=False
        result['Assetizable']=True
        result['Is Class']=''
        result['Additional Properties']=''
        result['Family']=''
        result['Type']=''
        result['Sub-Type']=''
        result['Scope']=''
        result['Parent Class']=''
        result['Qualification Context Rule Set']=''
        result['Lifecycle Details']=''
        result['Status']='Active'
        result['Selling Start Date']='01/01/2022'
        result['Selling End Date']=''
        result['Fulfillment Start Date']='01/01/2022'
        result['End of Life Date']=''
       
        resultlist.append(result)
    return resultlist

#Create a list of instances along with their attributes name and code
def ec2_attributes():
    print('Start EC2 Attributes Method')
    resultlist = []

    attributes=[{'Attribute Name': 'vCPU', 'Attribute Code': 'CRMA_ATTR_VCPU'}, {'Attribute Name': 'CPU credits/hr', 'Attribute Code': 'CRMA_ATTR_CPU_CREDITS'},
    {'Attribute Name': 'Memory', 'Attribute Code': 'CRMA_ATTR_VCPU'},{'Attribute Name': 'Storage', 'Attribute Code': 'CRMA_ATTR_Storage'},
    {'Attribute Name': 'Network Performance', 'Attribute Code': 'CRMA_ATTR_NET_PERFORM'}, {'Attribute Name': 'Dedicated EBS Bandwidth', 'Attribute Code': 'CRMA_ATTR_DED_EBS'}]

    instances = ['t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge', 
    'm4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge', 'm4.10xlarge', 'm4.16xlarge']

    for i in instances:
        for att in attributes:
            result = {}       
            result['Offering']=i
            result['Offering Code']="CRMA_" + "_".join(i.upper().split('.'))
            result['Attribute Name']=att['Attribute Name']
            result['Attribute Code']=att['Attribute Code']
            result['Display Name']=att['Attribute Name']
            resultlist.append(result)
    return resultlist


#Create Instances and Attributes List combined using this method and the method above (ec2_attributes)
def ec2_instances_and_attributes(region_name):
    print('Start EC2 Instances & Attributes Method')
    #Authorize AWS Calls
    ec2 = boto3.client('ec2', region_name=region_name, aws_access_key_id='AKIA5HMXIFKSOP6NZ6YB', aws_secret_access_key='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')
    resultlist = []
    #Perform AWS API Call
    describe_result = ec2.describe_instance_types( InstanceTypes=['t2.nano', 't2.micro', 't2.small', 't2.medium', 't2.large', 't2.xlarge', 't2.2xlarge', 't3.nano', 't3.micro', 't3.small', 't3.medium', 't3.large', 't3.xlarge', 't3.2xlarge', 'm4.large', 'm4.xlarge', 'm4.2xlarge', 'm4.4xlarge', 'm4.10xlarge', 'm4.16xlarge'])
    #Call the ec2_attributes Method in order to combine its results with this one
    attResults=ec2_attributes()

    #Construct the JSON to add in Google Sheets
    for i in describe_result['InstanceTypes']:
        memory = i['MemoryInfo']['SizeInMiB']/1024
        
        for att in attResults:
            attResult={}
            attResult['Status'] = 'Active'
            attResult['Effective Start Date'] = '01/01/2022'

            if (i['InstanceType'] == att['Offering']):
                if (att['Attribute Name'] == 'vCPU') :
                    result={}
                    result.update(att)
                    result['Value']=i['VCpuInfo']['DefaultVCpus']
                elif(att['Attribute Name'] == 'Memory'):
                    result={}
                    result.update(att)
                    result['Value']=memory
                elif(att['Attribute Name'] == 'Storage'):
                    result={}
                    result.update(att)
                    result['Value']= 'EBS-only'
                elif(att['Attribute Name'] == 'Network Performance'):
                    result={}
                    result.update(att)
                    result['Value']=i['NetworkInfo']['NetworkPerformance']
                elif(att['Attribute Name'] == 'Dedicated EBS Bandwidth' and 'EbsOptimizedInfo' in i['EbsInfo']):
                    result={}
                    result.update(att)
                    result['Value']=i['EbsInfo']['EbsOptimizedInfo']['BaselineBandwidthInMbps']
                result.update(attResult)
                resultlist.append(result)
    return resultlist