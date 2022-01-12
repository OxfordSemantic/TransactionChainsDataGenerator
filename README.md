# Transaction Chains Data Generator

## Generating data
For Help, run:
```python
python main.py --help
```

Generate data example:
Generate 10,000 transactions in 10 files, 1000 transaction per file
```python
python main.py -o data -tc $NUM_OF_MSG -pc $NUM_OF_PARTIES -mdb $MAX_DAYS_BEFORE -fc $NUM_OF_FILES -thc $THREAD_COUNT
python main.py -o data -tc 100000 -pc 1000 -mdb 3 -fc 100 -thc 10
```
Generate 5,000,000 transactions in 100 files, 50,000 transaction per file
```python
python main.py -o data -tc 5000000 -fc 100
```

This will create or overwrite the files in the 'data' folder.
