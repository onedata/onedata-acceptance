#!/usr/bin/env python3

"""
Runs integration and acceptance tests in docker environment.

All paths used are relative to script's path, not to the running user's CWD.
Run the script with -h flag to learn about script's running options.
"""

import re
import os
import sys
import glob
import platform
import argparse
from subprocess import *
import xml.etree.ElementTree as ElementTree

from bamboos.docker.environment import docker
from tests.utils.path_utils import get_default_image_for_service
from tests.utils.docker_utils import pull_docker_image_with_retries

TEST_RUNNER_CONTAINER_NAME = 'test-runner'


def get_images_option(test_type='oneclient', oz_image=None, op_image=None,
                      rest_cli_image=None, oc_image=None, luma_image=None):
    if test_type == 'upgrade':
        # in upgrade tests images are provided in test config and manually set are ignored
        return ''
    images_cfg = []
    add_image_to_images_cfg(oz_image, 'onezone', '--oz-image', images_cfg)
    add_image_to_images_cfg(op_image, 'oneprovider', '--op-image', images_cfg)
    add_image_to_images_cfg(rest_cli_image, 'rest cli', '--rest-cli-image',
                            images_cfg)

    if test_type in ['oneclient', 'mixed', 'onedata_fs', 'performance', 'upgrade']:
        add_image_to_images_cfg(oc_image, 'oneclient', '--oc-image',
                                images_cfg)
        add_image_to_images_cfg(luma_image, 'LUMA', '--luma-image', images_cfg)
    return ' + '.join(images_cfg)


def add_image_to_images_cfg(image, service_name, option, images_cfg):
    if image:
        print('Using image: {} for {} service'.format(image, service_name))
        pull_docker_image_with_retries(image)
        images_cfg.append("['{}={}']".format(option, image))


def load_test_report(junit_report_path):
    reports = glob.glob(junit_report_path)
    # if there are many reports, check only the last one
    if reports:
        reports.sort()
        tree = ElementTree.parse(reports[-1])
        testsuite = tree.getroot()
        return testsuite


def env_errors_exists(testsuite):
    testcases = testsuite.findall('testcase')

    for testcase in testcases:
        skipped = testcase.find('skipped')
        if skipped is not None:
            if re.match('.*environment error.*', skipped.attrib['message'].lower(),
                        re.I):
                return True
    return False


def clean_env(image, script_dir, kube_config_path, minikube_config_path,
              one_env_data_dir):
    reflect = [
        (script_dir, 'ro'),
        ('/var/run/docker.sock', 'rw'),
        (kube_config_path, 'ro'),
        (minikube_config_path, 'ro'),
        (one_env_data_dir, 'ro')
    ]

    docker.run(
        tty=True,
        rm=True,
        interactive=True,
        name='onenv-clean',
        workdir=os.path.join(script_dir, 'one_env'),
        reflect=reflect,
        network='host',
        image=image,
        envs={'HOME': os.path.expanduser('~')},
        command=['./onenv', 'clean', '-a', '-v']
    )

    container = docker.ps(all=True, quiet=True,
                          filters=[('name', TEST_RUNNER_CONTAINER_NAME)])
    if container:
        docker.remove(container, force=True)


def remove_one_env_container():
    container = docker.ps(all=True, quiet=True, filters=[('name', 'one-env')])
    if container:
        docker.remove(container, force=True)


def main():
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
        default=get_default_image_for_service('onezone'),
        dest='oz_image')

    parser.add_argument(
        '--op-image', '-pi',
        action='store',
        help='Oneprovider image to use in tests',
        default=get_default_image_for_service('oneprovider'),
        dest='op_image')

    parser.add_argument(
        '--oc-image', '-ci',
        action='store',
        help='Oneclient image to use in tests',
        default=get_default_image_for_service('oneclient'),
        dest='oc_image')

    parser.add_argument(
        '--rest-cli-image', '-ri',
        action='store',
        help='Rest cli image to use in tests',
        default=get_default_image_for_service('rest_cli'),
        dest='rest_cli_image')

    parser.add_argument(
        '--luma-image', '-li',
        action='store',
        help='Luma image to use in tests',
        default=get_default_image_for_service('luma'),
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
        default='~/.kube',
        dest='kube_config_path')

    parser.add_argument(
        '--minikube-config-path',
        action='store',
        help='Path to minikube config file',
        default='~/.minikube',
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
        '--pull-only-missing-images',
        action='store_true',
        help='By default all tests scenarios force pulling docker images '
             'even if they are already present on host machine. When this '
             'option is passed only missing images will be downloaded.',
        dest='pull_only_missing_images')

    [args, pass_args] = parser.parse_known_args()
    script_dir = os.path.abspath(os.path.join('..', os.path.dirname(os.path.abspath(__file__))))

    command = '''
import os, subprocess, sys, stat, shutil

{additional_code}

if {shed_privileges}:
    docker_gid = os.stat('/var/run/docker.sock').st_gid
    os.chmod('/etc/resolv.conf', 0o666)
    os.setgroups([docker_gid])
    os.setregid({gid}, {gid})
    os.setreuid({uid}, {uid})

command = ['python3'] + ['-m'] + ['pytest'] + ['-rs'] + ['-s'] + ['--test-type={test_type}'] + ['{test_dir}'] + {args} + {env_file} + {local_charts_path} + {no_clean} + {pull_only_missing_images} + {timeout} + {images_opt} + ['--junitxml={report_path}'] + ['--add-test-domain']

ret = subprocess.call(command)
sys.exit(ret)
'''

    images_opt = get_images_option(
        args.test_type,
        oz_image=args.oz_image,
        op_image=args.op_image,
        oc_image=args.oc_image,
        rest_cli_image=args.rest_cli_image,
        luma_image=args.luma_image
    )

    if args.update_etc_hosts:
        call(['./onenv', 'init'], cwd='one_env')
        call(['./onenv', 'hosts'], cwd='one_env')

    if args.local:
        # TODO: change this after python3 will be used in tests
        cmd = ['python3', '-m', 'pytest',
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

        command = command.format(
            args=pass_args,
            uid=os.geteuid(),
            gid=os.getegid(),
            test_dir=args.test_dir,
            shed_privileges=(platform.system() == 'Linux'),
            report_path=args.report_path,
            test_type=args.test_type,
            additional_code=additional_code,
            local_charts_path=['--local-charts-path={}'.format(args.local_charts_path)]
            if args.local_charts_path else [],
            no_clean=['--no-clean'] if not args.clean else [],
            env_file=['--env-file={}'.format(args.env_file)] if args.env_file else [],
            timeout=['--timeout={}'.format(args.timeout)] if args.timeout else [],
            images_opt=images_opt if images_opt else [],
            home=os.path.expanduser('~'),
            pull_only_missing_images=['--pull-only-missing-images'] if args.pull_only_missing_images else []
        )

        kube_config_path = os.path.expanduser(args.kube_config_path)
        minikube_config_path = os.path.expanduser(args.minikube_config_path)
        one_env_data_dir = os.path.expanduser(os.path.join('~', '.one-env'))
        docker_config_dir = os.path.expanduser(os.path.join('~', '.docker'))

        if args.clean:
            clean_env(args.image, script_dir, kube_config_path,
                      minikube_config_path, one_env_data_dir)
        remove_one_env_container()

        run_params = ['--shm-size=128m']
        reflect = [
            (script_dir, 'rw'),
            (docker_config_dir, 'ro'),
            ('/var/run/docker.sock', 'rw'),
            (one_env_data_dir, 'rw'),
            (kube_config_path, 'ro'),
            (minikube_config_path, 'ro'),
            ('/etc/passwd', 'ro')
        ]
        docker.run(
            tty=True,
            rm=True,
            interactive=True,
            name=TEST_RUNNER_CONTAINER_NAME,
            workdir=script_dir,
            network='host',
            reflect=reflect,
            image=args.image,
            command=['python', '-c', '{}'.format(command)],
            run_params=run_params,
            # setting HOME allows to use k8s and minikube configs
            # from host
            envs={'HOME': os.path.expanduser('~')}
        )

        if args.clean:
            clean_env(args.image, script_dir, kube_config_path,
                      minikube_config_path, one_env_data_dir)
        remove_one_env_container()

    report = load_test_report(args.report_path)
    # If exit code != 0 then bamboo always fails build.
    # If it is 0 then result is based on test report.
    ret = 0
    if env_errors_exists(report):
        ret = 1

    sys.exit(ret)


if __name__ == '__main__':
    main()
