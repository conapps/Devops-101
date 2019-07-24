import cdk = require('@aws-cdk/core');

import { Demo1 } from './stacks/Demo1';
import { Demo3 } from './stacks/Demo3';

const app = new cdk.App();
new Demo1(app, 'Demo1');
new Demo3(app, 'Demo3');
app.synth();