import argparse
import logging
import openml
import os
import sklearnbot
import random


# sshfs fr_jv1031@login1.nemo.uni-freiburg.de:/home/fr/fr_fr/fr_jv1031/experiments ~/nemo_experiments
def parse_args():
    all_classifiers = sklearnbot.config_spaces.get_available_config_spaces(True)
    parser = argparse.ArgumentParser(description='Generate data for openml-pimp project')
    parser.add_argument('--n_executions', type=int,  default=1000, help='number of runs to be executed. ')
    parser.add_argument('--study_id', type=str, default=14, help='the tag to obtain the tasks from')
    parser.add_argument('--openml_server', type=str, default=None, help='the openml server location')
    parser.add_argument('--openml_apikey', type=str, default=None, help='the apikey to authenticate to OpenML')
    parser.add_argument('--classifier_name', type=str, choices=all_classifiers, default='all',
                        help='the classifier to run')
    parser.add_argument('--scoring', type=str, default='predictive_accuracy', help='the evaluation measure of interest')
    default_output_dir = os.path.join(os.path.expanduser('~'), 'experiments/sklearn-bot')
    parser.add_argument('--output_dir', type=str, default=default_output_dir,
                        help='Location to store finished runs')
    parser.add_argument('--upload_result', action='store_true',
                        help='if true, results will be immediately uploaded to OpenML.'
                             'Otherwise they will be stored on disk. ')

    return parser.parse_args()


def run():
    root = logging.getLogger()
    root.setLevel(logging.INFO)

    args = parse_args()
    if args.openml_apikey:
        openml.config.apikey = args.openml_apikey
    if args.openml_server:
        openml.config.server = args.openml_server
    else:
        openml.config.server = 'https://test.openml.org/api/v1/'
    tasks = openml.study.get_study(args.study_id, 'tasks').tasks

    configuration_space = sklearnbot.config_spaces.get_config_space(args.classifier_name, None)
    output_dir = os.path.join(args.output_dir, args.classifier_name)

    for i in range(args.n_executions):
        task_id = random.choice(tasks)
        success, run_id, folder = sklearnbot.bot.run_bot_on_task(task_id,
                                                                 configuration_space,
                                                                 output_dir,
                                                                 args.upload_result)
        if success:
            logging.info('Run was executed successfully. Run id=%s; folder=%s' % (run_id, folder))
        else:
            logging.warning('A problem occurred. Run id=%s; folder=%s' % (run_id, folder))


if __name__ == '__main__':
    run()
