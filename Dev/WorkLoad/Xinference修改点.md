# Xinference修改点

## 修改点

### 1. `/v1/chat/completion` 接口强制返回/更新 usage

#### 1.1

- 修改 xinference/api/restful_api.py

```python
    async def create_chat_completion(self, request: Request) -> Response:
        raw_body = await request.json()
        body = CreateChatCompletion.parse_obj(raw_body)
        # .....
        kwargs = body.dict(exclude_unset=True, exclude=exclude)
        # 增加
        if kwargs.get("stream"):
            kwargs["stream_options"] = {"include_usage": "True"}
```

### 2. 添加累加统计参数

#### 2.1 111

- 修改 xinference/core/metrics.py

```python
generate_throughput = Gauge(
    "xinference:generate_tokens_per_s", "Generate throughput in tokens/s."
)
# Latency
# .....
# additional
generate_throughput_total_counter = Gauge(
    "xinference:generate_tokens_per_s_total_counter", "Cumulative generate throughput in tokens/s."
)
```

- 修改 xinference/core/model.py

```python
    async def _record_completion_metrics(
        self, duration, completion_tokens, prompt_tokens
    ):
        coros = []
        if completion_tokens > 0:
            coros.append(
                self.record_metrics(
                    "output_tokens_total_counter",
                    "add",
                    {
                        "labels": self._metrics_labels,
                        "value": completion_tokens,
                    },
                )
            )
        if prompt_tokens > 0:
            coros.append(
                self.record_metrics(
                    "input_tokens_total_counter",
                    "add",
                    {"labels": self._metrics_labels, "value": prompt_tokens},
                )
            )
        if completion_tokens > 0:
            generate_throughput = completion_tokens / duration
            coros.append(
                self.record_metrics(
                    "generate_throughput",
                    "set",
                    {
                        "labels": self._metrics_labels,
                        "value": generate_throughput,
                    },
                )
            )
            coros.append(
                self.record_metrics(
                    "cumulative_generate_throughput",
                    "add",
                    {
                        "labels": self._metrics_labels,
                        "value": generate_throughput,
                    },
                )
            )
        await asyncio.gather(*coros)
```

## 参考资料
