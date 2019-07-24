import ec2 = require('@aws-cdk/aws-ec2');
import cdk = require('@aws-cdk/core');

export class Cloud101VPC extends cdk.Construct {
  public readonly vpc: ec2.Vpc;
  
  constructor(scope: cdk.Construct, id: string) {
    super(scope, id);

    this.vpc = new ec2.Vpc(this, id, {
      cidr: '10.0.0.0/16',
      enableDnsHostnames: true,
      enableDnsSupport: true
    });
  }
}