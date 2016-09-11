import glob
import xml.etree.ElementTree
import fnmatch
import os
import sys


def find_dataset_definitions(dataset_folders):
    shared_datasets = {}
    for dataset_folder in dataset_folders:
        for f in glob.glob(dataset_folder + '*.xml'):
            r = xml.etree.ElementTree.parse(f).getroot()
            for ds in r.findall("dataset"):
                shared_datasets[ds.attrib['name']] = {'url': ds[0].text}
    return shared_datasets


def find_coordinator_definitions(coordinator_folders):
    # parse all coordinator.xml files for input- and output-events of
    coordinators = {}
    for src in coordinator_folders:
        for root, dirnames, filenames in os.walk(src):
            for filename in fnmatch.filter(filenames, 'coordinator.xml'):
                c = xml.etree.ElementTree.parse(root + "/" + filename).getroot()
                coord_name = root.split("/")[-2]
                coordinators[coord_name] = {'in': [], 'out': []}
                for e in c.iter():
                    if e.tag == '{uri:oozie:coordinator:0.1}data-in':
                        ds_name = e.attrib['dataset']
                        coordinators[coord_name]['in'].append(ds_name)
                    if e.tag == '{uri:oozie:coordinator:0.1}data-out':
                        ds_name = e.attrib['dataset']
                        coordinators[coord_name]['out'].append(ds_name)
    return coordinators


def build_edges(coordinators):
    edges = []
    for c, params in coordinators.items():
        for inputDs in params['in']:
            edges.append([inputDs, c])
        for outputDs in params['out']:
            edges.append([c, outputDs])
    return edges


def format_name(ce):
    return "\"" + ce.replace(".", ".") + "\""


def ds_style(url):
    return " [shape=folder color=slategray1 style=filled URL=\"%s\"];" % url


def coord_style(coord):
    return " [color=cornsilk style=filled]"


def print_dot_output(coordinators, datasets, edges):
    print("digraph Workflows {")
    print("  node[fontsize=11];")
    print("  edge[arrowsize=0.5 arrowhead=vee];")
    print()

    for coord in coordinators.keys():
        print("  " + format_name(coord) + coord_style(coord))

    print()

    for ds in datasets.keys():
        print("  " + format_name(ds) + ds_style(datasets[ds]["url"]))

    print()

    for edge in edges:
        print("  " + format_name(edge[0]) + " -> " + format_name(edge[1]) + ";")

    print("}")


def main():
    args = sys.argv
    dataset_folders = args[1].split(",")
    coordinator_folders = args[2].split(",")
    datasets = find_dataset_definitions(dataset_folders)
    coordinators = find_coordinator_definitions(coordinator_folders)
    edges = build_edges(coordinators)
    print_dot_output(coordinators, datasets, edges)


main()
