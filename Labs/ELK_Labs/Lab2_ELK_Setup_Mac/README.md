# Setting Up ELK Stack for Logging and Training a LR Model

In this lab, we will walk through the process of setting up the ELK (Elasticsearch, Logstash, Kibana) stack for log management and visualization while training a Linear Regression (LR) model.

## Prerequisites
Make sure you have the following prerequisites in place:

1. Java Installed: ELK stack requires Java to run. To check if Java is installed on your system, open your command line or terminal and run the following command:

```commandline
java -version
```
2. Java Home: Add the following line to your .bash_profile, replacing /path/to/java with the actual path you obtained in 

```commandline
/usr/libexec/java_home
```
```commandline
export JAVA_HOME = /path/to/java
```
Verify that JAVA_HOME is correctly set by running:
```commandline
echo $JAVA_HOME
```

# MacOS

Watch the tutorial on how to setup ELK on mac at [ELK Mac setup](https://www.youtube.com/watch?v=4Lux9ZX6J4Y)


## Elasticsearch
Elasticsearch is a distributed, RESTful search, and analytics engine.

#### Installation Steps:
- Visit the Elasticsearch download page: [Elasticsearch Download](https://www.elastic.co/downloads/elasticsearch)

- Select the appropriate version for your operating system (Windows, macOS).

- Download the Elasticsearch package for your system.

- Once the download is complete, extract the package to your preferred installation directory.

- Open a terminal window.

- Navigate to the Elasticsearch directory by using the `cd` command:
```commandline
cd /path/to/elasticsearch
```
- Once you are inside the Elasticsearch directory, go into the `bin` folder:
- Start Elasticsearch by running the following command:
```commandline
./elasticsearch
```
- After Elasticsearch has started successfully, open a web browser and visit the following URL
```plaintext
http://localhost:9200
```
- If Elasticsearch is functioning correctly, you should see JSON content displayed in your web browser.

- Add these two lines in the elasticsearch.yml file:
  - xpack.ml.enabled: false  
  - xpack.security.enabled: false
  - xpack.security.enrollment.enabled: false

## Kibana

Kibana is a powerful data visualization and exploration tool for Elasticsearch.

#### Installation Steps:
- Visit the Kibana download page: [Kibana Download](https://www.elastic.co/downloads/kibana)

- Select the appropriate version for your operating system (Windows, macOS).

- Download the Kibana package for your system.

- Once the download is complete, extract the package to your preferred installation directory.

- Open a terminal window.

- Navigate to the Kibana directory by using the `cd` command:
```commandline
cd /path/to/kibana
```
- Once you are inside the Kibana directory, go into the `bin` folder:
- Start Kibana by running the following command:
```commandline
./kibana
```
- If you are using Windows, use this command instead:
```commandline
.\kibana.bat
```
- After Kibana has started successfully, open a web browser and visit the following URL
```plaintext
http://localhost:5601
```
## Logstash
Logstash is a data processing pipeline tool that is often used in conjunction with Elasticsearch and Kibana to ingest, transform, and send data to Elasticsearch for indexing and storage.

#### Installation Steps:
- Visit the Logstash download page: [Logstash Download](https://www.elastic.co/downloads/logstash)

- Select the appropriate version for your operating system (Windows, macOS).

- Download the Logstash package for your system.

- Once the download is complete, extract the package to your preferred installation directory.

- Open a terminal window.
- To test the working of Logstash.

- Navigate to the Logstash directory by using the `cd` command:
```commandline
cd /path/to/logstash
```
- Start Logstash by running the following command:
```commandline
bin/logstash -e 'input{stdin{}} output{stdout{}}'
```
- This will prompt the user to provide input for which it returns a log in the terminal

## Logging
Let's setup the logging for the LR machine learning model and log the relevant information using the Python logging library to integrate with Logstash for centralized log management.
```python
logging.basicConfig(filename='training.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
This configuration ensures that log messages are written to the `training.log` file.

The following information will be logged:
- Start of model training.
- Number of training samples.
- Number of testing samples.
- Completion of model training.
- Model accuracy on test data.
- Model coefficients.
- Model intercept.

#### Logstash.conf

The `logstash.conf` file is a configuration file for Logstash, which is used to specify how Logstash should ingest, process, and output log data.

```plaintext
input {
  file {
    path => "/path/to/your/training.log"
    start_position => "beginning"
    sincedb_path => "/dev/null"
    codec => "json" 
  }
}
```

- `input`: This section specifies where Logstash should read log data from.

- `file`: It is an input plugin that reads data from a file.

- `path`: This field should be set to the path of the log file you want to ingest. In this example, it's set to "/path/to/your/training.log".

- `start_position`: This option specifies where Logstash should start reading the log file. "beginning" means it will start from the beginning of the file.

- `sincedb_path`: This option is used to store information about the current position in the log file. Setting it to "/dev/null" means that Logstash won't use a sincedb file, which is suitable for reading the entire file.

- `codec`: This field specifies the codec to use for parsing log data. In this example, it's set to "json", which implies that the log data is in JSON format.

```plaintext
filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{LOGLEVEL:loglevel} - %{GREEDYDATA:message}" }
  }
  mutate {
    rename => {
      "timestamp" => "log_timestamp"
      "loglevel" => "log_level"
      "message" => "log_message"
    }
  }
}
```

- `filter`: This section is used to process and transform the log data before it is sent to the output.

- `grok`: It is a filter plugin that allows you to extract structured data from unstructured log messages. In this example, it's used to parse the log message into structured fields.
- `match`: This field specifies the pattern to match in the log message using regular expressions. It extracts the timestamp, log level, and the remaining message text into separate fields.
- `mutate`: This filter plugin is used to perform various operations on fields.
- `rename`: It renames the fields extracted by the grok filter to more descriptive names, creating columns in the output data. For example, it renames "timestamp" to "log_timestamp," "loglevel" to "log_level," and "message" to "log_message."

```plaintext
output {
  elasticsearch {
    hosts => ["localhost:9200"]
    index => "logstash-training"
  }
  stdout {
    codec => rubydebug {
      metadata => false # Disable metadata to clean up the output
    }
  }
}
```

- `output`: This section defines where the processed log data should be sent.

- `elasticsearch`: It specifies that the log data should be sent to an Elasticsearch instance.

- `hosts`: This field should be set to the address and port of your Elasticsearch cluster. In this example, it's set to "localhost:9200".

- `index`: It defines the name of the Elasticsearch index where the log data will be stored. In this example, it's set to "logstash-training".

- `stdout`: This output plugin is used for debugging and displays log data to the console.

- `codec`: It specifies how the data should be formatted when displayed. In this case, it uses the rubydebug codec.

- `metadata`: It's set to false to disable including metadata in the console output, which helps keep the output clean.

#### Visualise the logs

To start Elasticsearch, Kibana, and Logstash and visualize logs in Kibana, follow these steps:

`Starting Elasticsearch:` 
- Open a terminal window.

- Navigate to the Elasticsearch directory by using the `cd` command:
```commandline
cd /path/to/elasticsearch
```
- Once you are inside the Elasticsearch directory, go into the `bin` folder:
- Start Elasticsearch by running the following command:
```commandline
./elasticsearch
```
- After Elasticsearch has started successfully, open a web browser and visit the following URL
```plaintext
http://localhost:9200
```

`Starting Kibana:` 
- Open a terminal window.

- Navigate to the Kibana directory by using the `cd` command:
```commandline
cd /path/to/kibana
```
- Once you are inside the Kibana directory, go into the `bin` folder:
- Start Kibana by running the following command:
```commandline
./kibana
```
- After Kibana has started successfully, open a web browser and visit the following URL
```plaintext
http://localhost:5601
```

`Starting Logstash:` 
- Open a terminal window.

- Navigate to the logstash directory by using the `cd` command:
```commandline
cd /path/to/logstash
```
- Once you are inside the Logstash directory, start Logstash by running the following command:
```commandline
bin/logstash -f /path/to/logstash.conf
```
Now, you can access and visualize the logs in Kibana under the `Discover` section.
