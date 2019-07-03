#!/usr/bin/env python3

"""
Runs integration and acceptance tests in docker environment.

All paths used are relative to script's path, not to the running user's CWD.
Run the script with -h flag to learn about script's running options.
"""

import re
import os
import sys
import json
import glob
import platform
import argparse
from subprocess import *
import xml.etree.ElementTree as ElementTree

from bamboos.docker.environment import docker
from one_env.scripts.utils import one_env_dir
from one_env.scripts.utils.terminal import info
from one_env.scripts.onenv_hosts import update_etc_hosts
from one_env.scripts.utils.one_env_dir import user_config
from one_env.scripts.utils.artifacts import LOCAL_ARTIFACTS_DIR


ZONE_IMAGES_CFG_PATH = 'onezone_images/docker-dev-build-list.json'
PROVIDER_IMAGES_CFG_PATH = 'oneprovider_images/docker-dev-build-list.json'
CLIENT_IMAGES_CFG_PATH = 'oneclient_images/oc-docker-dev-build-list.json'
LUMA_IMAGES_CFG_PATH = 'luma_images/luma-docker-build-report.json'
REST_CLI_IMAGES_CFG_PATH = 'rest_cli_images/rest-cli-docker-build-report.json'


def load_test_report(junit_report_path):
    reports = glob.glob(junit_report_path)
    # if there are many reports, check only the last one
    if reports:
        reports.sort()
        tree = ElementTree.parse(reports[-1])
        testsuite = tree.getroot()
        return testsuite


def skipped_test_exists(testsuite):
    if testsuite.attrib['skips'] != '0':
        return True
    return False


def env_errors_exists(testsuite):
    testcases = testsuite.findall('testcase')

    for testcase in testcases:
        skipped = testcase.find('skipped')
        if skipped is not None:
            if re.match('.*environment error.*', skipped.attrib['message'],
                        re.I):
                return True
    return False


def parse_image_for_service(file_path):
    abs_file_path = os.path.join(LOCAL_ARTIFACTS_DIR, file_path)
    try:
        with open(abs_file_path, 'r') as images_cfg_file:
            images = json.load(images_cfg_file)
            image = images.get('git-commit')
            return image
    except FileNotFoundError:
        return None


def delete_test_runner_pod():
    delete_test_runner_cmd = ['kubectl', 'delete', 'pod', 'test-runner']
    call(delete_test_runner_cmd, stdin=None, stderr=DEVNULL, stdout=DEVNULL)


def clean_env():
    docker.run(tty=True,
               rm=True,
               user=os.geteuid(),
               group=os.getegid(),
               interactive=True,
               name='onenv-clean',
               workdir=os.path.join(script_dir, 'one_env'),
               reflect=reflect,
               volumes=[(os.path.join(os.path.expanduser('~'),
                                      '.docker'), '/tmp/.docker', 'rw'),
                        (kube_config_path, '/tmp/.kube/config', 'rw'),
                        (minikube_config_path, '/tmp/.minikube/config', 'rw'),
                        (os.path.join(os.path.expanduser('~'), '.one-env'),
                         '/tmp/.one-env', 'rw')],
               image=args.image,
               command=['./onenv', 'clean', '-a', '-v'],
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
    default='tests/oneclient',
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
    default='oneclient',
    help='Type of test (oneclient, env_up, performance, packaging, gui)',
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
    default=parse_image_for_service(ZONE_IMAGES_CFG_PATH),
    dest='oz_image')

parser.add_argument(
    '--op-image', '-pi',
    action='store',
    help='Oneprovider image to use in tests',
    default=parse_image_for_service(PROVIDER_IMAGES_CFG_PATH),
    dest='op_image')

parser.add_argument(
    '--oc-image', '-ci',
    action='store',
    help='Oneclient image to use in tests',
    default=parse_image_for_service(CLIENT_IMAGES_CFG_PATH),
    dest='oc_image')

parser.add_argument(
    '--rest-cli-image', '-ri',
    action='store',
    help='Rest cli image to use in tests',
    default=parse_image_for_service(REST_CLI_IMAGES_CFG_PATH),
    dest='rest_cli_image')

parser.add_argument(
    '--luma-image', '-li',
    action='store',
    help='Luma image to use in tests',
    default=parse_image_for_service(LUMA_IMAGES_CFG_PATH),
    dest='luma_image')

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

parser.add_argument(
    '--privileged',
    action='store_true',
    help='Specifies if kubernetes pod should be run in privileged mode. '
         'This option is useful when using minikube with hypervisor.')

[args, pass_args] = parser.parse_known_args()

user_config.ensure_exists()

script_dir = os.path.dirname(os.path.abspath(__file__))

command = '''
import os, subprocess, sys, stat, shutil

{additional_code}

if {shed_privileges}:
    kube_path = '/tmp/.kube'
    if not os.path.exists(kube_path):
        os.makedirs(kube_path)
    shutil.copyfile(os.path.join('{home}', '.kube/config'), 
                    os.path.join(kube_path, 'config'))
    os.environ['HOME'] = '/tmp'
    docker_gid = os.stat('/var/run/docker.sock').st_gid
    os.chmod('/etc/resolv.conf', 0o666)
    os.chmod('/etc/hosts', 0o666)
    os.setgroups([docker_gid])
    if not {privileged}:
        os.setregid({gid}, {gid})
        os.setreuid({uid}, {uid})
        
command = ['python'] + ['-m'] + ['py.test'] + ['--test-type={test_type}'] + ['{test_dir}'] + {args} + {env_file} + {local_charts_path} + {no_clean} + {timeout} + {images_opt} + ['--junitxml={report_path}'] + ['--add-test-domain']  
ret = subprocess.call(command)
sys.exit(ret)
'''

oz_image, op_image, rest_cli_image = (args.oz_image, args.op_image,
                                      args.rest_cli_image)
images_cfg = []
if oz_image:
    info('Using onezone image: {}'.format(oz_image))
    docker.pull_image(oz_image)
    images_cfg.append("['--oz-image={}']".format(oz_image))
if op_image:
    info('Using oneprovider image: {}'.format(op_image))
    docker.pull_image(op_image)
    images_cfg.append("['--op-image={}']".format(op_image))
if rest_cli_image:
    info('Using rest cli image: {}'.format(rest_cli_image))
    docker.pull_image(rest_cli_image)
    images_cfg.append("['--rest-cli-image={}']".format(rest_cli_image))

if args.test_type in ['oneclient', 'mixed']:
    oc_image, luma_image = args.oc_image, args.luma_image
    if oc_image:
        info('Using oneclient image: {}'.format(oc_image))
        docker.pull_image(oc_image)
        images_cfg.append("['--oc-image={}']".format(oc_image))
    if luma_image:
        info('Using luma image: {}'.format(luma_image))
        docker.pull_image(luma_image)
        images_cfg.append("['--luma-image={}']".format(luma_image))
images_opt = ' + '.join(images_cfg)

if args.update_etc_hosts:
    update_etc_hosts()

if args.local:
    # TODO: change this after python3 will be used in tests
    cmd = ['python2.7', '-m', 'py.test',
           '--test-type={}'.format(args.test_type),
           args.test_dir, '--junitxml={}'.format(args.report_path),
           '--local'] + pass_args
    ret = call(cmd, stdin=None, stderr=None, stdout=None)

else:
    additional_code = '''
with open('/etc/sudoers.d/all', 'w+') as file:
    file.write("""
ALL       ALL = (ALL) NOPASSWD: ALL
""")
'''

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
                             images_opt=images_opt if images_opt else [],
                             home=one_env_dir.get_host_home(),
                             privileged=args.privileged)
    kube_config_path = os.path.expanduser(args.kube_config_path)
    minikube_config_path = os.path.expanduser(args.minikube_config_path)
    run_params = ['--shm-size=128m']
    reflect = [(script_dir, 'rw'),
               ('/var/run/docker.sock', 'rw'),
               ((os.path.join(os.path.expanduser('~'), '.minikube')), 'ro')]

    test_runner_pod = '''
{{
    "apiVersion": "v1",
    "spec": {{
        "securityContext": {{
            "privileged": {privileged}
        }},
        "containers": [
            {{
                "name": "test-runner",
                "image": "{image}",
                "stdin": {stdin},
                "tty": {tty},
                "imagePullPolicy": "IfNotPresent",
                "workingDir": "{script_dir}",
                "command" : [
                    "python"
                ],
                "args": [
                    "-c",
                    "{command}"
                ],
                "volumeMounts": [
                {{
                    "mountPath": "{script_dir}",
                    "name": "script-dir"
                }},
                {{
                    "mountPath": "/var/run/docker.sock",
                    "name": "docker-sock"
                }},
                {{
                    "mountPath": "/dev/shm",
                    "name": "shm"
                }},
                {{
                    "mountPath": "/etc/passwd",
                    "name": "etc-passwd",
                    "readOnly": true
                }},
                {{
                    "mountPath": "{home}/.kube/config",
                    "name": "kube-conf",
                    "readOnly": true
                }},                
                {{
                    "mountPath": "{home}/.minikube",
                    "name": "minikube-conf",
                    "readOnly": true
                }},                
                {{
                    "mountPath": "/tmp/.one-env",
                    "name": "one-env-data"
                }}
                ]
            }}
        ],
        "volumes": [
        {{
            "name": "script-dir",
            "hostPath": {{
                "path": "{minikube_script_dir}"
            }}
        }},
        {{
            "name": "docker-sock",
            "hostPath": {{
                "path": "/var/run/docker.sock"
            }}
        }},
        {{
            "name": "shm",
            "hostPath": {{
                "path": "/dev/shm"
            }}
        }},
        {{
            "name": "etc-passwd",
            "hostPath": {{
                "path": "/etc/passwd"
            }}
        }},
        {{
            "name": "kube-conf",
            "hostPath": {{
                "path": "{minikube_home}/.kube/config"
            }}
        }},       
        {{
            "name": "minikube-conf",
            "hostPath": {{
                "path": "{minikube_home}/.minikube"
            }}
        }},       
        {{
            "name": "one-env-data",
            "hostPath": {{
                "path": "{minikube_home}/.one-env"
            }}
        }}
        ]
    }}
}}
'''
    command = command.replace('\n', r'\n').replace('\"', '\'')
    try:
        kube_host_home_dir = user_config.get('kubeHostHomeDir')
    except FileNotFoundError:
        kube_host_home_dir = os.path.expanduser('~')

    minikube_script_dir = script_dir.replace(one_env_dir.get_host_home(),
                                             kube_host_home_dir)
    if sys.__stdin__.isatty():
        stdin = 'true'
        tty = 'true'
    else:
        stdin = 'false'
        tty = 'false'

    privileged = 'true' if args.privileged else 'false'
    test_runner_pod = test_runner_pod.format(command=command,
                                             script_dir=script_dir,
                                             minikube_script_dir=minikube_script_dir,
                                             image=args.image,
                                             home=os.path.expanduser('~'),
                                             minikube_home=kube_host_home_dir,
                                             privileged=privileged,
                                             stdin=stdin,
                                             tty=tty)

    cmd = ['kubectl', 'run', '-it', '--rm', '--restart=Never',
           'test-runner', '--overrides={}'.format(test_runner_pod),
           '--image={}'.format(args.image), '--', 'python', '-c',
           '"{}"'.format(command)]

    if args.clean:
        clean_env()
    delete_test_runner_pod()

    ret = call(cmd, stdin=None, stderr=None, stdout=None)

    if args.clean:
        clean_env()
    delete_test_runner_pod()

report = load_test_report(args.report_path)

if ret != 0 and not skipped_test_exists(report):
    ret = 0

if env_errors_exists(report):
    ret = 1

sys.exit(ret)
