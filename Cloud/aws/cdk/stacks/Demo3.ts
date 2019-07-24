import cdk = require('@aws-cdk/core');

import { Cloud101VPC } from '../constructs/Cloud101VPC';

export class Demo3 extends cdk.Stack {
  constructor(app: cdk.App, id: string) {
    super(app, id);

    new Cloud101VPC(this, 'VPC');
  }
}