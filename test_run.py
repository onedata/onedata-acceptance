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
import yaml

import glob
import xml.etree.ElementTree as ElementTree
import shutil
import one_env.scripts.user_config as user_config


def service_name_to_alias_mapping(name):
    return [val for key, val in
            {'oneprovider-krakow': 'oneprovider-1',
             'oneprovider-paris': 'oneprovider-2',
             'oneprovider-lisbon': 'oneprovider-3',
             'onezone': 'onezone'}.items() if key.lower() in name][0]


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


def horizontal_line():
    (width, _) = shutil.get_terminal_size()
    print('-' * width)


def run_onenv_command(command, args=None):
    cmd = ["./onenv", command]

    if args:
        cmd.extend(args)

    horizontal_line()
    print("Running command: {}".format(cmd))
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE, cwd="one_env")
    output, err = proc.communicate()

    sys.stdout.write(output.decode("utf-8"))
    sys.stderr.write(err.decode("utf-8"))

    return output


def parse_pods_cfg(pods_cfg):
    zone_config = {'name': "['--zone-name']",
                   'ip':  "['--zone-ip']",
                   'domain': "['--zone-hostname']",
                   'alias': "['--zone-alias']",
                   'container_id': "['--zone-container-id']"}

    providers_config = {'name': "['--providers-names']",
                        'ip': "['--providers-ips']",
                        'domain': "['--providers-hostnames']",
                        'alias': "['--providers-aliases']",
                        'container_id': "['--providers-containers-id']"}

    for pod, pod_cfg in pods_cfg.items():
        if pod_cfg['service-type'] == 'onezone':
            for opt in zone_config:
                if opt == 'alias':
                    zone_config[opt] += " + ['{}']".format(
                        service_name_to_alias_mapping(pod))
                else:
                    zone_config[opt] += " + ['{}']".format(pod_cfg[opt])
        else:
            for opt in providers_config:
                if opt == 'alias':
                    providers_config[opt] += " + ['{}']".format(
                        service_name_to_alias_mapping(pod))
                else:
                    providers_config[opt] += " + ['{}']".format(pod_cfg[opt])

    zone_conf = ""
    zone_params = list(zone_config.values())
    for param in zone_params[:-1]:
        zone_conf += "{} + ".format(param)
    zone_conf += zone_params[-1]

    providers_conf = ""
    providers_params = list(providers_config.values())
    for param in providers_params[:-1]:
        providers_conf += "{} + ".format(param)
    providers_conf += providers_params[-1]

    return zone_conf, providers_conf


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
    default="acceptance",
    help="Type of test (acceptance, env_up, performance, packaging, gui)",
    dest='test_type')

parser.add_argument(
    '--env-file', '-e',
    action='store',
    default=None,
    help="path to description of test environment in .json file",
    dest='env_file')

parser.add_argument(
    '--keywords', '-k',
    action='store',
    default='',
    help="path to description of test environment in .yaml file",
    dest='keywords')


[args, pass_args] = parser.parse_known_args()

script_dir = os.path.dirname(os.path.abspath(__file__))

command = '''
import os, subprocess, sys, stat

{additional_code}

if {shed_privileges}:
    os.environ['HOME'] = '/tmp'
    docker_gid = os.stat('/var/run/docker.sock').st_gid
    os.chmod('/etc/resolv.conf', 0o666)
    os.setgroups([docker_gid])
    os.setregid({gid}, {gid})
    os.setreuid({uid}, {uid})

command = ['py.test'] + ['--test-type={test_type}'] + ['{test_dir}'] + {args} + {keywords} + {env_file} + {zone_conf} + {providers_conf} + ['--junitxml={report_path}']  
ret = subprocess.call(command)
sys.exit(ret)
'''

additional_code = ''

additional_code += """
with open('/etc/sudoers.d/all', 'w+') as file:
    file.write('''
ALL       ALL = (ALL) NOPASSWD: ALL
''')
"""

test_runner_pod = '''{{
        "apiVersion": "v1",
        "spec": {{
            "containers": [
                {{
                    "name": "test-runer",
                    "image": "{image}",
                    "stdin": true, 
                    "tty": true,
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
            }}
            ]
        }}
}}'''

run_onenv_command("up", ["-f", "{}".format(
    os.path.join(script_dir, args.env_file))])
run_onenv_command("wait")

status_output = run_onenv_command("status")
status_output = yaml.load(status_output.decode("utf-8"))
pods_cfg = status_output["pods"]

oz_conf, ops_conf = parse_pods_cfg(pods_cfg)

command = command.format(args=pass_args,
                         uid=os.geteuid(),
                         gid=os.getegid(),
                         test_dir=args.test_dir,
                         shed_privileges=(platform.system() == "Linux"),
                         report_path=args.report_path,
                         test_type=args.test_type,
                         additional_code=additional_code,
                         env_file="[]",
                         zone_conf=oz_conf,
                         providers_conf=ops_conf,
                         keywords=["-k={}".format(
                             args.keywords)] if args.keywords else [])
command = command.replace("\n", r"\n").replace("\"", "\'")

minikube_script_dir = script_dir.replace(user_config.host_home(),
                                         user_config.get("kubeHostHomeDir"))
test_runner_pod = test_runner_pod.format(command=command,
                                         script_dir=script_dir,
                                         minikube_script_dir=minikube_script_dir,
                                         image=args.image)

cmd = ["kubectl"] + ["run"] + ["-it"] + ["--rm"] + ["--restart=Never"] + \
      ["test-runner"] + ["--overrides={}".format(test_runner_pod)] + \
      ["--image={}".format(args.image)] + ["--"] + ["python"] + ["-c"] + \
      ["\"{}\"".format(command)]

ret = call(cmd, stdin=None, stderr=None, stdout=None)

run_onenv_command("clean")

if ret != 0 and not skipped_test_exists(args.report_path):
    ret = 0

sys.exit(ret)
