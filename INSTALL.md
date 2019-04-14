The package supports python 3.7 for windows. To install the package:
   
   python setup.py develop

To access the prometheus monitoring, get prometheus 2.8.1 from https://prometheus.io/download/. Run prometheus with the --config.file=[prometheus.yml](prometheus.yml)

To view the Graphana dashboard, download version 6.1.3 from https://grafana.com/get. Setup the prometheus data source and import the dashboard configuration.
