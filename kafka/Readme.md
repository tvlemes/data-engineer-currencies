# Kafka - Configurando o Kafka

## **Criando o tópico do projeto**

Execute:
```yaml
docker exec data-engineer-kafka /opt/kafka/bin/kafka-topics.sh --create --topic finance.market --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

Depois liste os tópicos:
```yaml
docker exec data-engineer-kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092
```

Deve aparecer:
```yaml
finance.market
```

## **Testar o Kafka antes de integrar com FastAPI**

* Terminal 1 — consumidor
```yaml
docker exec -it data-engineer-kafka /opt/kafka/bin/kafka-console-consumer.sh --topic finance.market --bootstrap-server localhost:9092
```
Deixe esse terminal aberto.

* Terminal 2 — produtor
```yaml
docker exec -it data-engineer-kafka /opt/kafka/bin/kafka-console-producer.sh --topic finance.market --bootstrap-server localhost:9092
```

* Teste
```yaml
curl http://localhost:8000/api/v1/finances
```

* Ver os logs
```yaml
docker compose logs -f api
```