## 查看当前事务
```sql
SELECT * FROM information_schema.INNODB_TRX;
```

## 查看`innodb`日志状态
```sql
show engine innodb status;
```

```log

=====================================
2021-10-22 19:35:06 0x590c INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 1 seconds
-----------------
BACKGROUND THREAD
-----------------
srv_master_thread loops: 12 srv_active, 0 srv_shutdown, 281748 srv_idle
srv_master_thread log flush and writes: 0
----------
SEMAPHORES
----------
OS WAIT ARRAY INFO: reservation count 25
OS WAIT ARRAY INFO: signal count 25
RW-shared spins 0, rounds 0, OS waits 0
RW-excl spins 0, rounds 0, OS waits 0
RW-sx spins 0, rounds 0, OS waits 0
Spin rounds per wait: 0.00 RW-shared, 0.00 RW-excl, 0.00 RW-sx
------------
TRANSACTIONS
------------
Trx id counter 4940
Purge done for trx's n:o < 4893 undo n:o < 0 state: running but idle
History list length 0
LIST OF TRANSACTIONS FOR EACH SESSION:
---TRANSACTION 284071298771320, not started
0 lock struct(s), heap size 1128, 0 row lock(s)
---TRANSACTION 284071298770544, not started
0 lock struct(s), heap size 1128, 0 row lock(s)
---TRANSACTION 4939, ACTIVE 12 sec starting index read
mysql tables in use 1, locked 1
LOCK WAIT 2 lock struct(s), heap size 1128, 1 row lock(s)
MySQL thread id 17, OS thread handle 30600, query id 2295 localhost 127.0.0.1 root executing
/* ApplicationName=DataGrip 2021.2 */ SELECT * FROM book FOR UPDATE
------- TRX HAS BEEN WAITING 12 SEC FOR THIS LOCK TO BE GRANTED:
RECORD LOCKS space id 2 page no 4 n bits 120 index PRIMARY of table `db_example`.`book` trx id 4939 lock_mode X waiting
Record lock, heap no 2 PHYSICAL RECORD: n_fields 8; compact format; info bits 0
 0: len 8; hex 8000000000000bb8; asc         ;;
 1: len 6; hex 00000000053c; asc      <;;
 2: len 7; hex 81000000880110; asc        ;;
 3: len 12; hex e588bbe6848fe7bb83e4b9a0; asc             ;;
 4: SQL NULL;
 5: SQL NULL;
 6: len 5; hex 99aa6f0c29; asc   o );;
 7: len 5; hex 99aa6f0c29; asc   o );;

------------------
---TRANSACTION 4895, ACTIVE 20642 sec
2 lock struct(s), heap size 1128, 51 row lock(s)
MySQL thread id 18, OS thread handle 22796, query id 2322 localhost 127.0.0.1 root starting
/* ApplicationName=DataGrip 2021.2 */ show engine innodb status
--------
FILE I/O
--------
I/O thread 0 state: wait Windows aio (insert buffer thread)
I/O thread 1 state: wait Windows aio (log thread)
I/O thread 2 state: wait Windows aio (read thread)
I/O thread 3 state: wait Windows aio (read thread)
I/O thread 4 state: wait Windows aio (read thread)
I/O thread 5 state: wait Windows aio (read thread)
I/O thread 6 state: wait Windows aio (write thread)
I/O thread 7 state: wait Windows aio (write thread)
I/O thread 8 state: wait Windows aio (write thread)
I/O thread 9 state: wait Windows aio (write thread)
Pending normal aio reads: [0, 0, 0, 0] , aio writes: [0, 0, 0, 0] ,
 ibuf aio reads:, log i/o's:, sync i/o's:
Pending flushes (fsync) log: 0; buffer pool: 0
2435 OS file reads, 597 OS file writes, 240 OS fsyncs
0.00 reads/s, 0 avg bytes/read, 0.00 writes/s, 0.00 fsyncs/s
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 0, seg size 2, 0 merges
merged operations:
 insert 0, delete mark 0, delete 0
discarded operations:
 insert 0, delete mark 0, delete 0
Hash table size 2267, node heap has 1 buffer(s)
Hash table size 2267, node heap has 0 buffer(s)
Hash table size 2267, node heap has 0 buffer(s)
Hash table size 2267, node heap has 0 buffer(s)
Hash table size 2267, node heap has 0 buffer(s)
Hash table size 2267, node heap has 2 buffer(s)
Hash table size 2267, node heap has 2 buffer(s)
Hash table size 2267, node heap has 8 buffer(s)
0.00 hash searches/s, 0.00 non-hash searches/s
---
LOG
---
Log sequence number          18392883
Log buffer assigned up to    18392883
Log buffer completed up to   18392883
Log written up to            18392883
Log flushed up to            18392883
Added dirty pages up to      18392883
Pages flushed up to          18392883
Last checkpoint at           18392883
130 log i/o's done, 0.00 log i/o's/second
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 8572928
Dictionary memory allocated 460058
Buffer pool size   512
Free buffers       243
Database pages     256
Old database pages 0
Modified db pages  0
Pending reads      0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 0, not young 0
0.00 youngs/s, 0.00 non-youngs/s
Pages read 2410, created 151, written 337
0.00 reads/s, 0.00 creates/s, 0.00 writes/s
Buffer pool hit rate 1000 / 1000, young-making rate 0 / 1000 not 0 / 1000
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read ahead 0.00/s
LRU len: 256, unzip_LRU len: 0
I/O sum[1]:cur[0], unzip sum[0]:cur[0]
--------------
ROW OPERATIONS
--------------
0 queries inside InnoDB, 0 queries in queue
0 read views open inside InnoDB
Process ID=4084, Main thread ID=7148 , state=sleeping
Number of rows inserted 1, updated 1, deleted 0, read 462
0.00 inserts/s, 0.00 updates/s, 0.00 deletes/s, 0.00 reads/s
Number of system rows inserted 53, updated 325, deleted 12, read 19430
0.00 inserts/s, 0.00 updates/s, 0.00 deletes/s, 0.00 reads/s
----------------------------
END OF INNODB MONITOR OUTPUT
============================

```
