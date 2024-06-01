# ELK-Stack-Setup-in-Linux

Watch the toturial on how to Setup ELK on Windows WSL Ubuntu at [ELK installation](https://www.youtube.com/watch?v=UMjDYQO2lo0)

=========================
## Downloading:

### Elasticsearch: https://www.elastic.co/downloads/elasticsearch

### Kibana: https://www.elastic.co/downloads/kibana

### Logstash: https://www.elastic.co/downloads/logstash

### Java: https://www.oracle.com/java/technologies/downloads/

For elasticsearch version 8.12 you need to install Java version 21

==========================

## Moving the files

The files will be in Downloads you need to move it to Ubuntu.

To do that follow this step:

Change the directory to Downloads first and then run this:

```bash
cd /mnt/c/Users/(username)/Downloads
```

Move the tar files to Ubuntu:

```bash
sudo mv (name-of-the-files) /home
```

=======================

## Extracting:

Change directory to Ubuntu:

```bash
cd /home
```

Then extract them:

```bash
sudo tar -xzvf (name-of-the-files)
```

==============================

## Configure Environment Variables:

```bash
nano ~/.bashrc
```

Add this below and save them (Ctrl + S) and exit (Ctrl + X).

```bash
export JAVA_HOME=/home/jdk-21.0.2

export PATH=$JAVA_HOME/bin:$PATH
```

================================

Now to run them in Ubuntu we need to grant permissions:

```bash
sudo chown -R ayush:ayush /home/(kibana-8.12.0) OR (elasticsearch-8.12.0) OR (logstash-8.12.0)
```

Here, ayush is the username.

To add a new user, run this:

```bash
sudo adduser (username) 
```

Then run the above line.

============================

## Few steps to do before running the elk-stack:

### Generate Kibana Enrollment Token:

In a new terminal, navigate to the Elasticsearch bin directory:

```bash
cd path/to/elasticsearch/bin
```

Run the command:

```bash
./elasticsearch-create-enrollment-token --scope kibana
```

Copy and save the generated token.

========================

Enter Enrollment Token in Kibana:

Paste the enrollment token into the Kibana configuration interface in your browser.

========================

### Reset Elasticsearch Password:

In a new terminal, navigate to the Elasticsearch bin directory.

Run the password reset command:

```bash
./elasticsearch-reset-password -u elastic
```

Note down the newly generated password.

==============================

## Running the stack:

For elasticsearch go to this directory:

```bash
cd /home/elasticsearch-8.12.0/bin
```

Then run this:

```bash
./elasticsearch
```

=======================

For kibana go to this directory:

```bash
cd /home/kibana-8.12.0/bin
```

Then run this:

```bash
./kibana
```

========================

You might encounter an error when running Kibana, try this:

```bash
sudo ./kibana --allow-root
```

(P.S. This error only came once for me)

========================

For logstash go to this directory:

```bash
cd /home/logstash-8.12.0
```

Then run this:

```bash
bin/logstash -e 'input{stdin{}} output{stdout{}}'
```




