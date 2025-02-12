import click
from ec2_manager import ec2
from s3_manager import s3
from route53_manager import route53

@click.group()
def cli():
    """AWS Resource Provisioning CLI"""
    pass

cli.add_command(ec2)
cli.add_command(s3)
cli.add_command(route53)

if __name__ == "__main__":
    cli()
