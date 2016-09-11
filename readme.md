This Python script realizes a very simple approach for generating a Graphviz graph (dot format) for visualization of coordinator/workflow and dataset dependencies. The output is created by scanning the local filesystem for oozie-dataset and -coordinator definitions.

``python3 oozie-viz-graph.py <comma-separated-list-of-dataset-folders> <comma-separated-list-of-coordinator-folders>``

Output will be printed the stdout. Redirect this to a file of your choice and run Graphviz's dot command to create an SVG file (or similar):

``dot -Tsvg <dotfile> > oozie-deps.svg``
