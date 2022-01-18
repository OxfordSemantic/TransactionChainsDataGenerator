# Transaction Chains Data Generator
This is a random data generation program for the "Financial Crime Discovery using Amazon EKS and Graph Databases" article by Zahi Ben Shabat, in which he describes how to use [RDFox](https://www.oxfordsemantic.tech/product) and its reasoning capabilities to detect suspicious patterns in banking data.

The program is meant to simulate a record of bank transactions between individuals. It first generates a configurable number of parties, some of which are marked as "suspicious", and then a configurable number of transactions between them. Each transaction's "originator party" and "beneficiary party" are selected entirely randomly from the pool, and the transaction amount is also random. The program outputs RDF files in [Turtle](https://www.w3.org/TR/turtle/) syntax.

RDFox can find transactions involving "suspicious" individuals and follow "transaction chains" originating from them to find instances where money is being funneled from one criminal to another through a number of seemingly legitimate accounts (also known as money laundering).

RDFox is the world's most performant knowledge graph and reasoning engine. To try it for yourself, request a free trial [here](https://www.oxfordsemantic.tech/tryrdfoxforfree).

## Generating data
For Help, run:
```python
python main.py --help
```

Usage:
```python
python main.py -o data -tc $NUM_OF_MSG -pc $NUM_OF_PARTIES -mdb $MAX_DAYS_BEFORE -fc $NUM_OF_FILES -thc $THREAD_COUNT
```
This will create or overwrite the files in the 'data' folder.

## Examples

Generate 10,000 transactions in 10 files, 1000 transaction per file
```python
python main.py -o data -tc 100000 -pc 1000 -mdb 3 -fc 100 -thc 10
```

Generate 5,000,000 transactions in 100 files, 50,000 transaction per file
```python
python main.py -o data -tc 5000000 -fc 100
```


