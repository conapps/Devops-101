import cdk = require('@aws-cdk/core');

import { Cloud101EC2Instance } from '../constructs/Cloud101EC2Instance';

export class Demo1 extends cdk.Stack {
  constructor(app: cdk.App, id: string) {
    super(app, id);

    new Cloud101EC2Instance(this, 'PrivateInstance', {
      associatePublicIpAddress: true,
      availabilityZone: 'us-east-1a',
      name: 'private_instance'
    })
  }
}