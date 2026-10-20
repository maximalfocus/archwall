A jump host, or bastion, is the one server you can reach from outside. You sign in there, and only from there do you reach the private servers. One door is easier to lock and to watch.

**Two ways through.** With `ssh -J jump target` the jump host only forwards bytes, and you sign in to the target yourself. Or you log in to the jump host and run ssh from its shell. That ssh command runs on the jump host, but sshd only logs the sign-in. Recording commands takes extra tools. Pass-through needs TCP forwarding on the jump host, which AWS's reference template turns off by default.

![](hop.svg)

**Lock the door.** On the jump host's sshd: only listed users, no passwords, a key plus a second factor, forwarding only to listed targets, idle channels closed. Each accepted login is logged with its key and address.

![](sshd.svg)

**Certificates.** Instead of copying keys to every server, a CA signs each person's key with a name. Add an end date with -V; by default there is none. Servers trust the CA. A lost key goes on a revocation list.

![](certs.svg)

**On AWS.** The aws-ia Linux bastion templates run 1 to 4 bastions, 1 by default, over two subnets. The new-VPC template puts those in two zones. By default they sit in private subnets with no open port, and you come in through Session Manager. Set an address range and they go in public subnets with an Elastic IP, and SSH from that range is allowed. The audit log goes to CloudWatch.

![](aws.svg)

Sources: OpenSSH at commit 6a46ea6 and aws-ia/cfn-ps-linux-bastion at commit 213dd9a.
