# ELK-Stack-Setup-in-Linux

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

=> cd /mnt/c/Users/(username)/Downloads

Move the tar files to Ubuntu:

=> sudo mv (name-of-the-files) /home

=======================

## Extracting:

Change directory to Ubuntu:

=> cd /home

Then extract them:

=> sudo tar -xzvf (name-of-the-files)

==============================

## Configure Environment Variables:

=> nano ~/.bashrc

Add this below and save them (Ctrl + S) and exit (Ctrl + X).

export JAVA_HOME=/home/jdk-21.0.2

export PATH=$JAVA_HOME/bin:$PATH

================================

Now to run them in Ubuntu we need to grant permissions:

=> sudo chown -R ayush:ayush /home/(kibana-8.12.0) OR (elasticsearch-8.12.0) OR (logstash-8.12.0)

Here, ayush is the username.

To add a new user, run this:

sudo adduser (username) 

Then run the above line.

============================

## Few steps to do before running the elk-stack:

### Generate Kibana Enrollment Token:

In a new terminal, navigate to the Elasticsearch bin directory:

=> cd path/to/elasticsearch/bin

Run the command:

=> ./elasticsearch-create-enrollment-token --scope kibana

Copy and save the generated token.

========================

Enter Enrollment Token in Kibana:

Paste the enrollment token into the Kibana configuration interface in your browser.

========================

### Reset Elasticsearch Password:

In a new terminal, navigate to the Elasticsearch bin directory.

Run the password reset command:

=> ./elasticsearch-reset-password -u elastic

Note down the newly generated password.

==============================

## Running the stack:

For elasticsearch go to this directory:

=> cd /home/elasticsearch-8.12.0/bin

Then run this:

=> ./elasticsearch

=======================

For kibana go to this directory:

=> cd /home/kibana-8.12.0/bin

Then run this:

=> ./kibana

========================

You might encounter an error when running Kibana, try this:

=> sudo ./kibana --allow-root

(P.S. This error only came once for me)

========================

For logstash go to this directory:

=> cd /home/logstash-8.12.0

Then run this:

=> bin/logstash -e 'input{stdin{}} output{stdout{}}'





