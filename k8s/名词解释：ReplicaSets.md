# 什么是 ReplicaSet

ReplicaSet 是下一代复本控制器。ReplicaSet 和 Replication Controller 之间的唯一区别是现在的选择器支持。
Replication Controller 只支持基于等式的 selector（env=dev 或 environment!=qa），
但 ReplicaSet 还支持新的，基于集合的 selector（version in (v1.0, v2.0)或 env notin (dev, qa)）。

虽然 ReplicaSets 可以独立使用，但是今天它主要被 Deployments 作为协调 pod 创建，删除和更新的机制。
当您使用 Deployments 时，您不必担心管理他们创建的 ReplicaSets。Deployments 拥有并管理其 ReplicaSets。

## 何时使用 ReplicaSet

ReplicaSet 可确保指定数量的 pod“replicas”在任何设定的时间运行。
然而，Deployments 是一个更高层次的概念，它管理 ReplicaSets，并提供对 pod 的声明性更新以及许多其他的功能。
因此，我们建议您使用 Deployments 而不是直接使用 ReplicaSets，除非您需要自定义更新编排或根本不需要更新。

这实际上意味着您可能永远不需要操作 ReplicaSet 对象：直接使用 Deployments 并在规范部分定义应用程序。
