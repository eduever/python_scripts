'''
Author: rpeta
1)Get Tagname from dynamodb based on dag_emr_name as key
2)Get Instance fleet config by passing type,emrversion,clustertype,corememory,taskmemory,timedurationwait,block_duration_minutes

Usage:

GetDagConfig(Instance_series ,emr version,'ondemand/instancefleet', corememory, taskmemory,wait_time_interval,block_duration)

# code to be included in dag

sys.path.append("/app/bin/common/airflow_deploy/scripts/")
from get_dag_config import *
dagconf=GetDagConfig('r','5.9.0','ondemand', 600, 800,15,240)


# Tagging

tag_name=dagconf.getEmrTag("emr_dag_name",'dev')

#Instance Fleet

instance_fleet=dagconf.getIntancefleetConfig()

'''

from __future__ import print_function  # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr
import math
from emr_client.models.instance_fleet import InstanceFleet
from emr_client.models.instance_type_config import InstanceTypeConfig
from emr_client.models.launch_specification import LaunchSpecification
from emr_client.models.spot_specification import SpotSpecification
import sys
import collections
import json

sys.path.append('/app/bin/common/airflow_deploy/scripts/')

import instancefleet

class GetDagConfig(object):
	
	def __init__(self, type, emrversion, clustertype, corememory, taskmemory=0, timedurationwait=15,
			block_duration_minutes=None):
		self.type = type
		self.emrversion = emrversion
		self.corememory = corememory
		self.taskmemory = taskmemory
		self.timedurationwait = timedurationwait
		self.block_duration_minutes = block_duration_minutes
		self.clustertype = clustertype
	
	'''
	instance_conf={
		'r': {
			'r3.2xlarge': [1,'5.7.0']
			,'r3.4xlarge':[1,'5.7.0']
			,'r3.8xlarge':[1,'5.7.0']
			,'r5d.4xlarge':[1,'5.13.0']
		},
		'i':{
			'i3.2xlarge': [1,'5.7.0']
			,'i3.4xlarge':[2,'5.7.0']
			,'i3.8xlarge':[3,'5.7.0']
		}

	}'''
	
	'''read intance fleet config from config file'''
	
	instance_config = instancefleet.instance_conf
	mfactor = instancefleet.multi_factor
	
	'''function call to dynamodb  input: emr_dag_name,environment  return: tag_name'''
	
	def getEmrTag(self, dag_emr_name, env):
		dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		dag_emr_name = dag_emr_name
		env = env
		if env=='dev':
			dtable = 'dev_dtc_dag_config'
		elif env=='qa':
			dtable = 'qa_dtc_dag_config'
		else:
			dtable = 'prod_dtc_dag_config'
		table = dynamodb.Table(dtable)
		response = table.query(KeyConditionExpression=Key('dag_emr_name').eq(dag_emr_name))
		
		for i in response['Items']:
			return json.loads(str(i['tag_name']))
		else:
			return 'UNKNOWN'  # print ("no entry for the dag name" + dag_emr_name)  # sys.exit(1)
	
	'''function call to dynamodb  input: emr_dag_name,environment  return: tag_name'''
	
	def getEmrTags(self, dag_emr_name, env):
		dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
		dag_emr_name = dag_emr_name
		env = env
		ret_val = ''
		if env=='dev':
			dtable = 'eda-dev_dag_config'
		elif env=='qa':
			dtable = 'eda-qa_dag_config'
		else:
			dtable = 'eda-prod_dag_config'
		table = dynamodb.Table(dtable)
		response = table.query(KeyConditionExpression=Key('dag_emr_name').eq(dag_emr_name))
		default_val = '[{\"Key\": \"product\", \"Value\": \"default\"}]'
		for i in response['Items']:
			ret_val = json.loads(str(i['tag_name']))
		if len(ret_val)==0:
			return default_val
		else:
			return ret_val
	
	''' returns number of core and task nodes'''
	
	def getNumInstances(self, corememory, taskmemory=0, mf=61):
		if taskmemory!=0:
			(x, y) = (int(math.ceil(float(corememory) / mf)), int(math.ceil(float(taskmemory) / mf)))
		else:
			(x, y) = (int(math.ceil(float(corememory) / mf)), 0)
		return x, y
	
	'''Checks if the dag emr version supports instance minimum emr version'''
	
	def emrVersionCheck(self, emrversion_i, supportversion_i):
		emr_version = emrversion_i.split('.')
		support_version = supportversion_i.split('.')
		if emr_version[0]==support_version[0]:
			if int(support_version[1]) <= int(emr_version[1]):
				return True
			else:
				return False
		else:
			return False
	
	''' Function to return instance fleeet config '''
	
	def getInstanceFleetConfig(self):
		
		'''condition check for type of instances
		exampe: r --> rseries, m  --> mseries ,i --> iseries '''
		
		if self.type in self.instance_config:
			conf_temp = self.instance_config[self.type]
			conf = collections.OrderedDict(sorted(conf_temp.items(), reverse=True))
			instance_type_configs = []
			for instance_type in conf.keys():
				if self.emrVersionCheck(self.emrversion, conf[instance_type][1]):
					instance_type_conf = InstanceTypeConfig(bid_price_as_percentage_of_on_demand_price=100,
							instance_type=instance_type, weighted_capacity=conf[instance_type][0])
					
					instance_type_configs.append(instance_type_conf)
		else:
			raise ValueError("Unsupported instance type '{}' requested".format(self.type))
		
		instance_fleet_master = InstanceFleet(instance_fleet_type="MASTER", target_on_demand_capacity=1,
				instance_type_configs=[InstanceTypeConfig(instance_type="r5d.2xlarge", weighted_capacity=1)
				
				])
		# print("master created")
		if self.clustertype=='ondemand':
			launch_specifications = LaunchSpecification(
					spot_specification=SpotSpecification(timeout_action="SWITCH_TO_ON_DEMAND",
							timeout_duration_minutes=0))
		else:
			launch_specifications = LaunchSpecification(
					spot_specification=SpotSpecification(timeout_action="SWITCH_TO_ON_DEMAND",
							timeout_duration_minutes=self.timedurationwait,
							block_duration_minutes=self.block_duration_minutes))
		
		if self.taskmemory!=0:
			# print("core nodes and task nodes requested")
			t1 = self.corememory
			t2 = self.taskmemory
			mf = self.mfactor[self.type]
			corespotcapacity, taskspotcapacity = self.getNumInstances(t1, t2, mf)
			if self.clustertype=='ondemand':
				instance_fleet_task = InstanceFleet(instance_fleet_type="TASK",
						target_on_demand_capacity=taskspotcapacity, instance_type_configs=instance_type_configs,
						launch_specifications=launch_specifications)
				
				instance_fleet_core = InstanceFleet(instance_fleet_type="CORE",
						target_on_demand_capacity=corespotcapacity, instance_type_configs=instance_type_configs,
						launch_specifications=launch_specifications)
				
				instance_fleets = [instance_fleet_master, instance_fleet_core, instance_fleet_task]
			else:
				instance_fleet_task = InstanceFleet(instance_fleet_type="TASK", target_spot_capacity=taskspotcapacity,
						instance_type_configs=instance_type_configs, launch_specifications=launch_specifications)
				
				instance_fleet_core = InstanceFleet(instance_fleet_type="CORE", target_spot_capacity=corespotcapacity,
						instance_type_configs=instance_type_configs, launch_specifications=launch_specifications)
				
				instance_fleets = [instance_fleet_master, instance_fleet_core, instance_fleet_task]
		else:
			if self.clustertype=='ondemand':
				# print ("no task nodes")
				corespotcapacity, taskspotcapacity = self.getNumInstances(self.corememory)
				instance_fleet_core = InstanceFleet(instance_fleet_type="CORE",
						target_on_demand_capacity=corespotcapacity, instance_type_configs=instance_type_configs,
						launch_specifications=launch_specifications)
			else:
				# print ("no task nodes")
				corespotcapacity, taskspotcapacity = self.getNumInstances(self.corememory)
				instance_fleet_core = InstanceFleet(instance_fleet_type="CORE", target_spot_capacity=corespotcapacity,
						instance_type_configs=instance_type_configs, launch_specifications=launch_specifications)
			instance_fleets = [instance_fleet_master, instance_fleet_core]
		return instance_fleets

# Sample Json

"""
[
{'instance_fleet_type': 'MASTER',
 'instance_type_configs': [{'bid_price_as_percentage_of_on_demand_price': None,
                            'instance_type': 'r3.2xlarge',
                            'weighted_capacity': None}],
 'launch_specifications': None,
 'target_on_demand_capacity': 1,
 'target_spot_capacity': None}
 ,
 {'instance_fleet_type': 'CORE',
 'instance_type_configs': [{'bid_price_as_percentage_of_on_demand_price': 100,
                            'instance_type': 'r3.8xlarge',
                            'weighted_capacity': 3},
                           {'bid_price_as_percentage_of_on_demand_price': 100,
                            'instance_type': 'r3.2xlarge',
                            'weighted_capacity': 1},
                           {'bid_price_as_percentage_of_on_demand_price': 100,
                            'instance_type': 'r3.4xlarge',
                            'weighted_capacity': 2}],
 'launch_specifications': {'spot_specification': {'block_duration_minutes': None,
                                                  'timeout_action': 'SWITCH_TO_ON_DEMAND',
                                                  'timeout_duration_minutes': 5}},'target_on_demand_capacity': None,'target_spot_capacity': 10},

 {'instance_fleet_type': 'TASK',
 'instance_type_configs': [{'bid_price_as_percentage_of_on_demand_price': 100,
                            'instance_type': 'r3.8xlarge',
                            'weighted_capacity': 3},
                           {'bid_price_as_percentage_of_on_demand_price': 100,
                            'instance_type': 'r3.2xlarge',
                            'weighted_capacity': 1},
                           {'bid_price_as_percentage_of_on_demand_price': 100,
                            'instance_type': 'r3.4xlarge',
                            'weighted_capacity': 2}],
 'launch_specifications': {'spot_specification': {'block_duration_minutes': None,
                                                  'timeout_action': 'SWITCH_TO_ON_DEMAND',
                                                  'timeout_duration_minutes': 5}},
 'target_on_demand_capacity': None,
 'target_spot_capacity': 14}]
"""