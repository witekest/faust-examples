# faust-examples

## How to run

### Install [Faust](https://faust.readthedocs.io)

```
# vitrualenv -p python3 venv
# . venv/bin/activate
# pip install faust
```

### Start Zookeeper and Kafka

```
# $KAFKA_HOME/bin/zookeeper-server-start $KAFKA_HOME/etc/kafka/zookeeper.properties
# $KAFKA_HOME/bin/kafka-server-start $KAFKA_HOME/etc/kafka/server.properties
```

### Create topics

```
# $KAFKA_HOME/bin/kafka-topics.sh --create \
    --partitions 4 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092 \
    --topic hopping_topic
# $KAFKA_HOME/bin/kafka-topics.sh --create \
    --partitions 4 \
    --replication-factor 1 \
    --bootstrap-server localhost:9092 \
    --topic windowing-values_table-changelog
```

### Start worker

```
# faust -A windowed_aggregations worker -l info
```
