import ec2 = require('@aws-cdk/aws-ec2');
import cdk = require('@aws-cdk/core');

export interface Cloud101EC2InstanceProps {
  availabilityZone?: string;
  associatePublicIpAddress?: boolean;
  name?: string;
}

export class Cloud101EC2Instance extends cdk.Construct {
  public readonly instance: ec2.CfnInstance;
  
  constructor(scope: cdk.Construct, id: string, props: Cloud101EC2InstanceProps = {}) {
    super(scope, id);

    this.instance = new ec2.CfnInstance(this, id, {
      availabilityZone: props.availabilityZone || 'us-east-1a',
      imageId: 'ami-0b898040803850657',
      instanceType: 't2.small',
      networkInterfaces: [{
        deviceIndex: '0',
        associatePublicIpAddress: props.associatePublicIpAddress || true
      }],
      keyName: 'cdh',
      tags: [{
        key: 'Project',
        value: 'cloud_101'
      }, {
        key: 'Name',
        value: props.name || 'cloud_101_cdk_instance'
      }]
    });
  }
}