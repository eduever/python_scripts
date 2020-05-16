#instance fleet config file to add new instance types

emr_version_57='5.7.0'
emr_version_513='5.13.0'

instance_conf={
        'r': {
             'r5d.2xlarge':[1,emr_version_513]
            ,'r5d.4xlarge':[2,emr_version_513]
            ,'r3.2xlarge': [1,emr_version_57]
            ,'r3.4xlarge':[2,emr_version_57]
            ,'r3.8xlarge':[4,emr_version_57]
        },
        'i':{
            'i3.2xlarge': [1,emr_version_57]
            ,'i3.4xlarge':[2,emr_version_57]
            ,'i3.8xlarge':[4,emr_version_57]
            ,'i3.16xlarge':[8,emr_version_57]
        },
        'm': {
            'm5d.2xlarge':[1,emr_version_513]
            ,'m5d.4xlarge':[2,emr_version_513]
	}

    }

multi_factor={'r':61,'i': 61,'m':32}