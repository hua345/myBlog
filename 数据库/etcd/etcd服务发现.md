### etcd单元测试

#### 初始化etcd

```go
import (
    "fmt"
    "go.etcd.io/etcd/clientv3"
    "time"
)

var EtcdClient *clientv3.Client
func InitEtcd() {
    var err error
    EtcdClient, err = clientv3.New(clientv3.Config{
        Endpoints:   []string{"192.168.137.128:2379", "192.168.137.128:22379", "192.168.137.128:32379"},
        DialTimeout: 5 * time.Second,
    })
    if err != nil {
        panic(fmt.Sprintf("Unable to create etcd client: %v", err))
    }
}
```

#### etcd Put/Get单元测试

```golang
func TestEtcdPutGet(t *testing.T) {
    InitEtcd()
    testkey := "name"
    testValue := "fang"
    _, err := EtcdClient.Put(context.Background(), testkey, testValue)
    if err != nil {
        t.Log("Etcd Put Error")
        t.Error(err)
    }
    etcdResp, err := EtcdClient.Get(context.Background(), testkey)
    if err != nil {
        t.Error(err)
    }
    t.Log(etcdResp)
    t.Log(etcdResp.Kvs)
    if len(etcdResp.Kvs) != 0 {
        if testValue != string(etcdResp.Kvs[0].Value){
            t.Error("Put/Get值不一致")
        }
    }
}
```

测试结果

```golang
=== RUN   TestEtcdPutGet
--- PASS: TestEtcdPutGet (0.03s)
    etcd_test.go:21: &{cluster_id:8144621041877720777 member_id:5025925290928334777 revision:50 raft_term:2  [key:"name" create_revision:47 mod_revision:50 version:4 value:"fang" ] false 1}
    etcd_test.go:22: [key:"name" create_revision:47 mod_revision:50 version:4 value:"fang" ]
PASS
```
