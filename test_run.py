#!/usr/bin/env python3

"""
Runs integration and acceptance tests in docker environment.

All paths used are relative to script's path, not to the running user's CWD.
Run the script with -h flag to learn about script's running options.
"""

import argparse
import os
import platform
import sys
from subprocess import *
import json

import glob
import xml.etree.ElementTree as ElementTree
from one_env.scripts.console import info
from tests.test_type import map_test_type_to_logdir
from environment import docker, dockers_config
from one_env.scripts.update_etc_hosts import update_etc_hosts


ZONE_IMAGES_CFG_PATH = 'onezone_images/docker-dev-build-list.json'
PROVIDER_IMAGES_CFG_PATH = 'oneprovider_images/docker-dev-build-list.json'


def skipped_test_exists(junit_report_path):
    reports = glob.glob(junit_report_path)
    # if there are many reports, check only the last one
    if reports:
        reports.sort()
        tree = ElementTree.parse(reports[-1])
        testsuite = tree.getroot()
        if testsuite.attrib['skips'] != '0':
            return True
    return False


def parse_image_for_service(file_path, ):
    try:
        with open(file_path, 'r') as images_cfg_file:
            images = json.load(images_cfg_file)
            image = images.get('git-branch')
            return image
    except FileNotFoundError:
        return None


def parse_images():
    if args.oz_image:
        oz_image = args.oz_image
    else:
        oz_image = parse_image_for_service(ZONE_IMAGES_CFG_PATH)

    if args.op_image:
        op_image = args.op_image
    else:
        op_image = parse_image_for_service(PROVIDER_IMAGES_CFG_PATH)

    if oz_image:
        info('Using onezone image: {}'.format(oz_image))
    if op_image:
        info('Using oneprovider image: {}'.format(op_image))

    return oz_image, op_image


def clean_env():
    docker.run(tty=True,
               rm=True,
               interactive=True,
               name='test-runner',
               workdir=os.path.join(script_dir, 'one_env'),
               reflect=reflect,
               volumes=[(os.path.join(os.path.expanduser('~'),
                                      '.docker'), '/tmp/.docker', 'rw'),
                        (kube_config_path, '/tmp/.kube/config', 'rw'),
                        (minikube_config_path, '/tmp/.minikube/config', 'rw'),
                        (os.path.join(os.path.expanduser('~'),
                                      '.one-env'), '/tmp/.one-env', 'rw')],
               image=args.image,
               command=['./onenv', 'clean'],
               envs={'HOME': '/tmp'})


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    description='Run Common Tests.')

parser.add_argument(
    '--image', '-i',
    action='store',
    default='onedata/worker',
    help='Docker image to use as a test master.',
    dest='image')

parser.add_argument(
    '--test-dir', '-t',
    action='store',
    default='tests/acceptance',
    help='Test dir to run.',
    dest='test_dir')

parser.add_argument(
    '--report-path', '-r',
    action='store',
    default='test-reports/results.xml',
    help='Path to JUnit tests report',
    dest='report_path')

parser.add_argument(
    '--test-type', '-tt',
    action='store',
    default='acceptance',
    help='Type of test (acceptance, env_up, performance, packaging, gui)',
    dest='test_type')

parser.add_argument(
    '--env-file', '-e',
    action='store',
    help='Path to description of test environment in .yaml file',
    dest='env_file')

parser.add_argument(
    '--no-clean', '-n',
    action='store_false',
    help='If present prevents cleaning environment created by one-env',
    dest='clean')

parser.add_argument(
    '--local', '-l',
    action='store_true',
    help='If present runs test on host',
    dest='local')

parser.add_argument(
    '--oz-image', '-zi',
    action='store',
    help='Onezone image to use in tests',
    dest='oz_image')

parser.add_argument(
    '--op-image', '-pi',
    action='store',
    help='Oneprovider image to use in tests',
    dest='op_image')

parser.add_argument(
    '--update-etc-hosts', '-uh',
    action='store_true',
    help='If present adds entries to /etc/hosts on host machine for all zone '
         'and provider nodes in current deployment',
    dest='update_etc_hosts')

parser.add_argument(
    '--kube-config-path',
    action='store',
    help='Path to kube config file',
    default='~/.kube/config',
    dest='kube_config_path')

parser.add_argument(
    '--minikube-config-path',
    action='store',
    help='Path to minikube config file',
    default='~/.minikube/config',
    dest='minikube_config_path')

parser.add_argument(
    '--local-charts-path',
    action='store',
    help='Path to local charts that will be used by onenv',
    dest='local_charts_path')

parser.add_argument(
    '--timeout',
    action='store',
    help='Onenv wait timeout',
    dest='timeout')

[args, pass_args] = parser.parse_known_args()

script_dir = os.path.dirname(os.path.abspath(__file__))

command = '''
import os, subprocess, sys, stat

{additional_code}

if {shed_privileges}:
    os.environ['HOME'] = '/tmp'
    docker_gid = os.stat('/var/run/docker.sock').st_gid
    os.chmod('/etc/resolv.conf', 0o666)
    os.chmod('/etc/hosts', 0o666)
    os.setgroups([docker_gid])
    os.setregid({gid}, {gid})
    os.setreuid({uid}, {uid})

command = ['python'] + ['-m'] + ['py.test'] + ['--test-type={test_type}'] + ['{test_dir}'] + {args} + {env_file} + {local_charts_path} + {no_clean} + {timeout} + ['--oz-image={oz_image}'] + ['--op-image={op_image}'] + ['--junitxml={report_path}'] + ['--add-test-domain']  
ret = subprocess.call(command)
sys.exit(ret)
'''


oz_image, op_image = parse_images()

if args.update_etc_hosts:
    update_etc_hosts()

if args.local:
    # TODO: change this after python3 will be used in tests
    cmd = ['python2.7', '-m', 'py.test',
           '--test-type={}'.format(args.test_type),
           args.test_dir, '--junitxml={}'.format(args.report_path)]
    ret = call(cmd, stdin=None, stderr=None, stdout=None)

else:
    if args.test_type in ['gui', 'mixed_swaggers']:
        additional_code = '''
with open('/etc/sudoers.d/all', 'w+') as file:
    file.write("""
ALL       ALL = (ALL) NOPASSWD: ALL
""")
    '''
    else:
        additional_code = ''

    command = command.format(args=pass_args,
                             uid=os.geteuid(),
                             gid=os.getegid(),
                             test_dir=args.test_dir,
                             shed_privileges=(
                                     platform.system() == 'Linux'),
                             report_path=args.report_path,
                             test_type=args.test_type,
                             additional_code=additional_code,
                             local_charts_path=['--local-charts-path={}'.format(args.local_charts_path)]
                             if args.local_charts_path else [],
                             no_clean=['--no-clean'] if not args.clean else [],
                             env_file=['--env-file={}'.format(args.env_file)]
                             if args.env_file else [],
                             timeout=['--timeout={}'.format(args.timeout)]
                             if args.timeout else [],
                             oz_image=oz_image if oz_image else '',
                             op_image=op_image if op_image else '')
    kube_config_path = os.path.expanduser(args.kube_config_path)
    minikube_config_path = os.path.expanduser(args.minikube_config_path)
    run_params = ['--shm-size=128m']
    reflect = [(script_dir, 'rw'),
               ('/var/run/docker.sock', 'rw'),
               ((os.path.join(os.path.expanduser('~'), '.minikube')), 'ro')]

    if args.clean:
        clean_env()

    ret = docker.run(tty=True,
                     rm=True,
                     interactive=True,
                     name='test-runner',
                     workdir=script_dir,
                     reflect=reflect,
                     volumes=[(os.path.join(os.path.expanduser('~'),
                                            '.docker'), '/tmp/.docker', 'rw'),
                              (kube_config_path, '/tmp/.kube/config', 'rw'),
                              (minikube_config_path, '/tmp/.minikube/config', 'rw'),
                              (os.path.join(os.path.expanduser('~'),
                                            '.one-env'), '/tmp/.one-env', 'rw')],
                     image=args.image,
                     command=['python', '-c', command],
                     run_params=run_params)

    if args.clean:
        clean_env()

if ret != 0 and not skipped_test_exists(args.report_path):
    ret = 0

sys.exit(ret)
