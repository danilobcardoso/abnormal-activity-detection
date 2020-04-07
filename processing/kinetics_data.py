#!/usr/bin/python3
import argparse
import json
import os
from shutil import copyfile


def filter_by_label(label_info, selected_labels):
    filtered = {}
    for key in label_info.keys():
        label = label_info[key]['label']
        if label in selected_labels:
            filtered[key] = label_info[key]
    return filtered


def find_and_count_labels(label_path, p, selected_labels):
    print(label_path)
    print('Labels count for the [ {} ] dataset.'.format(p.upper()))
    label_count = {}
    label_instances = {}
    with open(label_path) as f:
        label_info = json.load(f)
        for key in label_info.keys():
            label = label_info[key]['label']
            if label in label_count:
                label_count[label] = label_count[label] + 1
                label_instances[label].append(key)
            else:
                label_count[label] = 1
                label_instances[label] = [key]

    if len(selected_labels) > 0:
        for label in selected_labels:
            print('{} \t {}'.format(label, label_count[label]))
    else:
        for label in sorted(label_count.keys()):
            print('{} \t {}'.format(label, label_count[label]))


def update_label_index(filtered_info, selected_labels):
    for key in filtered_info.keys():
        label = filtered_info[key]['label']
        index = selected_labels.index(label)
        filtered_info[key]['label_index'] = index


def find_and_slice_labels(source_data_path, source_label_path, target_data_path, target_label_path, p, selected_labels):
    print(source_label_path)
    print(target_label_path)
    if not os.path.exists(target_data_path):
        os.makedirs(target_data_path)

    with open(source_label_path) as input:
        label_info = json.load(input)
        filtered_info = filter_by_label(label_info, selected_labels)
        update_label_index(filtered_info, selected_labels)

        with open(target_label_path, 'w') as output:
            json.dump(filtered_info, output, indent=3)

        for key in filtered_info.keys():
            source_file = '{}/{}.json'.format(source_data_path, key)
            target_file = '{}/{}.json'.format(target_data_path, key)
            copyfile(source_file, target_file)


def process_count_labels(arg):
    part = ['train', 'val']
    for p in part:
        label_path = '{}/kinetics_{}_label.json'.format(arg.data_path, p)
        find_and_count_labels(label_path, p, arg.labels)


def process_slice_labels(arg):
    part = ['train', 'val']
    for p in part:
        source_label_path = '{}/kinetics_{}_label.json'.format(arg.data_path, p)
        source_data_path = '{}/kinetics_{}'.format(arg.data_path, p)
        target_label_path = '{}/kinetics_{}_label.json'.format(arg.output_path, p)
        target_data_path = '{}/kinetics_{}'.format(arg.output_path, p)
        find_and_slice_labels(source_data_path, source_label_path, target_data_path, target_label_path, p, arg.labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Skeleton data processing utility', epilog='Hope I`ve been helpfull! See`ya')
    parser.add_argument('operation', choices=['count_labels', 'slice_labels'])
    parser.add_argument('--data_path', nargs=1, help='Path to data to be processed', default='data/raw/kinetics-skeleton')
    parser.add_argument('--output_path', help='Path to write data after processing', default='data/raw/kinetics-skeleton/slice/temp')
    parser.add_argument('--labels', nargs='*', help='Labels to be processed', default='')
    args = parser.parse_args()
    if args.operation == 'count_labels':
        process_count_labels(args)
    elif args.operation == 'slice_labels':
        process_slice_labels(args)
        print('Im a filter')
    else:
        print('Im nothing')