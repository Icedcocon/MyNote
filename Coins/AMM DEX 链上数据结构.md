# AMM DEX 链上数据结构

### 1. 核心数据结构

#### 1.1 流动性池 (LiquidityPool)

- 结构

```typescript
interface LiquidityPool {
  // 代币储备
  coin_x_reserve: {
    value: string  // 代币X的数量
  }
  coin_y_reserve: {
    value: string  // 代币Y的数量
  }

  // AMM 核心参数
  k_last: string   // 恒定乘积 k = x * y

  // 价格累计器
  last_price_x_cumulative: string  // X代币累计价格
  last_price_y_cumulative: string  // Y代币累计价格

  // 时间戳
  last_block_timestamp: string

  // 安全控制
  locked: boolean  // 重入锁

  // LP代币控制
  lp_mint_cap: { dummy_field: boolean }  // 铸造权限
  lp_burn_cap: { dummy_field: boolean }  // 销毁权限
  lp_freeze_cap: { dummy_field: boolean }  // 冻结权限
}
```

- 例子1

```json
  {
    "type": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c::AnimeSwapPoolV1::LiquidityPool<0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5::staked_coin::StakedAptos>, 0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0x84d7aeef42d38a5ffc3ccef853e1b82e4958659d16a7de736a29c55fbbeb0114::staked_aptos_coin::StakedAptosCoin>>",
    "data": {
      "coin_x_reserve": {
        "value": "9693865"
      },
      "coin_y_reserve": {
        "value": "9769630"
      },
      "k_last": "94705474319950",
      "last_block_timestamp": "1666884549",
      "last_price_x_cumulative": "0",
      "last_price_y_cumulative": "0",
      "locked": false,
      "lp_burn_cap": {
        "dummy_field": false
      },
      "lp_freeze_cap": {
        "dummy_field": false
      },
      "lp_mint_cap": {
        "dummy_field": false
      }
    }
  }
```

###### (1) 流动性池说明

在 Aptos 上有两种不同类型的流动性池：

- 普通代币对流动性池

```rust
LiquidityPool<CoinA::T, CoinB::T>
```

  这种池子用于普通代币之间的交换，比如 APT-USDT, BTC-USDT 等。这里的 coin::T 是 Aptos 中代币的标准类型。

- LP代币对流动性池

```rust
LiquidityPool<
    LPCoin<CoinA, CoinB>,
    LPCoin<CoinC, CoinD>
>
```

这种池子用于 LP 代币之间的交换。LPCoinV1::LPCoin 是专门用于表示流动性提供者代币的类型。

###### (1) type字段结构分解1

```json
0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c::AnimeSwapPoolV1::LiquidityPool<
    0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<
        0x1::aptos_coin::AptosCoin,
        0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5::staked_coin::StakedAptos
    >,
    0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<
        0x1::aptos_coin::AptosCoin,
        0x84d7aeef42d38a5ffc3ccef853e1b82e4958659d16a7de736a29c55fbbeb0114::staked_aptos_coin::StakedAptosCoin
    >
>
```

**type字段结构说明**

- 基本格式：
  
     `{合约地址}::{模块名}::{结构体名}<{泛型参数}>`

- 各部分含义：

- 0x16fe2d... - AnimeSwap合约地址

- AnimeSwapPoolV1 - 模块名

- LiquidityPool - 结构体名

- <...> - 泛型参数列表

- 具体分层：
  
     LiquidityPool<LP1, LP2>
  
       LP1 = LPCoin<AptosCoin, StakedAptos>
  
       LP2 = LPCoin<AptosCoin, StakedAptosCoin>

**业务含义**

这个类型实际上表示的是：

- 这是一个流动性池，用于交易两种LP代币

- 这两种LP代币分别是：

- LP代币1：AptosCoin-StakedAptos的LP代币

- LP代币2：AptosCoin-StakedAptosCoin的LP代币

也就是说，这是一个LP代币对LP代币的流动性池，而不是普通代币对。这种设计允许用户直接在不同的LP代币之间进行交换，这在DeFi中被称为"LP代币对"或"复合流动性池"。

简单来说：

- 这不是普通的代币交易池（比如APT-USDT）

- 这是一个用于交易两种LP代币的特殊池子

- 这种设计可能用于优化流动性管理或提供更复杂的交易策略

###### (2) type字段结构分解2

#### 1.2 管理配置 (AdminData)

- 结构

```typescript
interface AdminData {
  // 管理权限
  admin_address: string
  signer_cap: {
    account: string
  }

  // 费用设置
  swap_fee: string        // 交易费率
  dao_fee: number        // DAO费率
  dao_fee_on: boolean    // 是否启用DAO费
  dao_fee_to: string     // DAO费用接收地址

  // 紧急控制
  is_pause: boolean      // 是否暂停
}
```

- 例子

```json
  {
    "type": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c::AnimeSwapPoolV1::AdminData",
    "data": {
      "admin_address": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c",
      "dao_fee": 5,
      "dao_fee_on": true,
      "dao_fee_to": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c",
      "is_pause": false,
      "signer_cap": {
        "account": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf"
      },
      "swap_fee": "30"
    }
  }
```

### 2. 事件系统

#### 2.1 事件记录 (Events)

- 结构

```typescript
interface Events {
  // LP代币事件
  mint_event: {
    counter: string
    guid: { id: { addr: string, creation_num: string } }
  }
  burn_event: {
    counter: string
    guid: { id: { addr: string, creation_num: string } }
  }

  // 交易事件
  swap_event: {
    counter: string
    guid: { id: { addr: string, creation_num: string } }
  }

  // 其他事件
  flash_swap_event: EventInfo
  pair_created_event: EventInfo
  sync_event: EventInfo
}
```

- 例子

```json
  {
    "type": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c::AnimeSwapPoolV1::Events<0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5::staked_coin::StakedAptos>, 0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0x84d7aeef42d38a5ffc3ccef853e1b82e4958659d16a7de736a29c55fbbeb0114::staked_aptos_coin::StakedAptosCoin>>",
    "data": {
      "burn_event": {
        "counter": "0",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "1294"
          }
        }
      },
      "flash_swap_event": {
        "counter": "0",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "1297"
          }
        }
      },
      "mint_event": {
        "counter": "1",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "1293"
          }
        }
      },
      "pair_created_event": {
        "counter": "1",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "1292"
          }
        }
      },
      "swap_event": {
        "counter": "0",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "1295"
          }
        }
      },
      "sync_event": {
        "counter": "1",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "1296"
          }
        }
      }
    }
  }
```

### 3. 代币相关

#### 3.1 代币信息 (CoinInfo)

- 结构

```typescript
interface CoinInfo {
  decimals: number      // 精度
  name: string         // 名称
  symbol: string       // 符号
  supply: {
    vec: [{
      aggregator: { vec: [] }
      integer: {
        vec: [{
          limit: string   // 最大供应量
          value: string   // 当前供应量
        }]
      }
    }]
  }
}
```

- 例子

```json
  {
    "type": "0x1::coin::CoinInfo<0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5::staked_coin::StakedAptos>, 0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0x84d7aeef42d38a5ffc3ccef853e1b82e4958659d16a7de736a29c55fbbeb0114::staked_aptos_coin::StakedAptosCoin>>>",
    "data": {
      "decimals": 8,
      "name": "AnimeSwapLPCoin",
      "supply": {
        "vec": [
          {
            "aggregator": {
              "vec": []
            },
            "integer": {
              "vec": [
                {
                  "limit": "340282366920938463463374607431768211455",
                  "value": "9731673"
                }
              ]
            }
          }
        ]
      },
      "symbol": "ANILPCoin"
    }
  }
```

#### 3.2 代币账户 (CoinStore)

- 结构

```typescript
interface CoinStore {
  coin: {
    value: string    // 余额
  }
  frozen: boolean    // 是否冻结

  // 存款事件
  deposit_events: {
    counter: string
    guid: { id: { addr: string, creation_num: string } }
  }

  // 提款事件
  withdraw_events: {
    counter: string
    guid: { id: { addr: string, creation_num: string } }
  }
}
```

- 例子

```json
  {
    "type": "0x1::coin::CoinStore<0x1::aptos_coin::AptosCoin>",
    "data": {
      "coin": {
        "value": "100000"
      },
      "deposit_events": {
        "counter": "1",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "2130"
          }
        }
      },
      "frozen": false,
      "withdraw_events": {
        "counter": "0",
        "guid": {
          "id": {
            "addr": "0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf",
            "creation_num": "2131"
          }
        }
      }
    }
  }
```

### 4. 交易对信息

#### 4.1 交易对注册表 (PairInfo)

```typescript
interface PairInfo {
  pair_list: Array<{
    coin_x: CoinType      // X代币类型
    coin_y: CoinType      // Y代币类型
    lp_coin: CoinType     // LP代币类型
  }>
}

interface CoinType {
  account_address: string
  module_name: string
  struct_name: string
}
```

### 5. 基础系统结构

#### 5.1 账户结构 (Account)

- 结构

```typescript
interface Account {
  // 账户的身份验证密钥
  authentication_key: string

  // 代币注册事件
  coin_register_events: {
    counter: string
    guid: {
      id: {
        addr: string
        creation_num: string
      }
    }
  }

  // GUID创建计数
  guid_creation_num: string

  // 密钥轮换事件
  key_rotation_events: {
    counter: string
    guid: {
      id: {
        addr: string
        creation_num: string
      }
    }
  }

  // 轮换能力授权
  rotation_capability_offer: {
    for: {
      vec: string[]
    }
  }

  // 交易序列号
  sequence_number: string

  // 签名能力授权
  signer_capability_offer: {
    for: {
      vec: string[]
    }
  }
}
```

#### 5.2 合约包注册表 (PackageRegistry)

- 结构

```typescript
interface PackageRegistry {
  packages: Array<{
    // 包依赖
    deps: Array<{
      account: string      // 账户地址
      package_name: string // 包名称
    }>

    // 扩展字段
    extension: {
      vec: any[]
    }

    // 包清单
    manifest: string

    // 模块列表
    modules: Array<{
      extension: {
        vec: any[]
      }
      name: string     // 模块名称
      source: string   // 源代码
      source_map: string
    }>

    // 包名称
    name: string

    // 源代码摘要
    source_digest: string

    // 升级编号
    upgrade_number: string

    // 升级策略
    upgrade_policy: {
      policy: number
    }
  }>
}
```

#### 5.3 扩展交易对信息 (ExtendedPairInfo)

- 结构

```typescript
interface ExtendedPairInfo {
  pair_list: Array<{
    // X代币信息(基础代币)
    coin_x: {
      account_address: string  // 代币合约地址
      module_name: string      // 模块名称
      struct_name: string      // 结构名称
    }

    // Y代币信息(交易代币)
    coin_y: {
      account_address: string
      module_name: string
      struct_name: string
    }

    // LP代币信息
    lp_coin: {
      account_address: string
      module_name: string
      struct_name: string
    }
  }>
}
```

这些基础系统结构的主要作用：

- Account 结构
  
  - 管理账户的身份验证和权限
  - 追踪账户相关事件
  - 维护交易序列号
  - 控制账户能力授权

- PackageRegistry 结构
  
  - 记录已部署的智能合约包
  - 管理包依赖关系
  - 存储模块源代码
  - 控制合约升级策略

- ExtendedPairInfo 结构
  
  - 定义交易对的完整配置
  - 记录交易代币的详细信息
  - 关联对应的LP代币信息
  - 支持多交易对管理

### 主要功能说明：

- 价格发现机制
  
  - 通过 coin_x_reserve 和 coin_y_reserve 计算实时价格
  
  - 使用 k_last 维护恒定乘积公式 (x y = k)

- 流动性管理
  
  - LP代币的铸造和销毁权限控制
  
  - 流动性提供者的份额追踪

- 费用系统
  
  - 交易费率设置 (swap_fee)
  
  - DAO费用分配机制

- 安全机制
  
  - 重入锁保护 (locked)
  
  - 紧急暂停功能 (is_pause)
  
  - 事件追踪系统

这种数据结构设计确保了：

- 交易的原子性和安全性

- 流动性的精确计算

- 费用的准确分配

- 完整的事件追踪

- 灵活的管理控制

## 二、交易所流动性池结构体列表

### 1. 列表

### 1.0 请求地址与编号

```bash
https://fullnode.mainnet.aptoslabs.com/v1/accounts/0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf/resources?limit=9999
# 关键字段：  coin_x_reserve、 coin_y_reserve
# 交易所编号：9 (anime_swap)

https://fullnode.mainnet.aptoslabs.com/v1/accounts/0xbd35135844473187163ca197ca93b2ab014370587bb0ed3befff9e902d6bb541/resources?limit=9999
# 关键字段：  x_reserve、 y_reserve
# 交易所编号：8 (aux_exchange)

https://fullnode.mainnet.aptoslabs.com/v1/accounts/0xec42a352cc65eca17a9fa85d0fc602295897ed6b8b8af6a6c79ef490eb8f9eba/resources?limit=9999
# 关键字段：  coin_a、 coin_b
# 交易所编号：10 (cetus_amm)

https://fullnode.mainnet.aptoslabs.com/v1/accounts/0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa/resources?limit=9999
# 关键字段：  reserve_x、 reverse_y
# 交易所编号：11（pancake_swap）

https://fullnode.mainnet.aptoslabs.com/v1/accounts/0xa5d3ac4d429052674ed38adc62d010e52d7c24ca159194d17ddc196ddb7e480b/resources?limit=9999
# 关键字段：  x、 
交# 交易所编号：易所编号：7 （aptoswap）
```

#### 1.1 anime_swap（9）

- 需要的池

```json
    {
        "type": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c::AnimeSwapPoolV1::LiquidityPool<0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::T, 0xae478ff7d83ed072dbc5e264250e67ef58f57c99d89b447efd8a0a2e8b2be76e::coin::T>",
        "data": {
            "coin_x_reserve": {
                "value": "4502525"
            },
            "coin_y_reserve": {
                "value": "4490"
            },
            "k_last": "19216832096",
            "last_block_timestamp": "1733547748",
            "last_price_x_cumulative": "3654720042113953442341337",
            "last_price_y_cumulative": "529982779127938275136396805406",
            "locked": false,
            "lp_burn_cap": {
                "dummy_field": false
            },
            "lp_freeze_cap": {
                "dummy_field": false
            },
            "lp_mint_cap": {
                "dummy_field": false
            }
        }
    }
```

- 排除的池

```json
  {
    "type": "0x16fe2df00ea7dde4a63409201f7f4e536bde7bb7335526a35d05111e68aa322c::AnimeSwapPoolV1::LiquidityPool<0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0xd11107bdf0d6d7040c6c0bfbdecb6545191fdf13e8d8d259952f53e1713f61b5::staked_coin::StakedAptos>, 0x796900ebe1a1a54ff9e932f19c548f5c1af5c6e7d34965857ac2f7b1d1ab2cbf::LPCoinV1::LPCoin<0x1::aptos_coin::AptosCoin, 0x84d7aeef42d38a5ffc3ccef853e1b82e4958659d16a7de736a29c55fbbeb0114::staked_aptos_coin::StakedAptosCoin>>",
    "data": {
      "coin_x_reserve": {
        "value": "9693865"
      },
      "coin_y_reserve": {
        "value": "9769630"
      },
      "k_last": "94705474319950",
      "last_block_timestamp": "1666884549",
      "last_price_x_cumulative": "0",
      "last_price_y_cumulative": "0",
      "locked": false,
      "lp_burn_cap": {
        "dummy_field": false
      },
      "lp_freeze_cap": {
        "dummy_field": false
      },
      "lp_mint_cap": {
        "dummy_field": false
      }
    }
  }
```

#### 1.2 aux_exchange（8）

```json
    {
        "type": "0xbd35135844473187163ca197ca93b2ab014370587bb0ed3befff9e902d6bb541::amm::Pool<0x6312bc0a484bc4e37013befc9949df2d7c8a78e01c6fe14a34018449d136ba86::coin::T, 0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::T>",
        "data": {
            "add_liquidity_events": {
                "counter": "0",
                "guid": {
                    "id": {
                        "addr": "0xbd35135844473187163ca197ca93b2ab014370587bb0ed3befff9e902d6bb541",
                        "creation_num": "205"
                    }
                }
            },
            "fee_bps": "10",
            "frozen": false,
            "lp_burn": {
                "dummy_field": false
            },
            "lp_mint": {
                "dummy_field": false
            },
            "remove_liquidity_events": {
                "counter": "0",
                "guid": {
                    "id": {
                        "addr": "0xbd35135844473187163ca197ca93b2ab014370587bb0ed3befff9e902d6bb541",
                        "creation_num": "206"
                    }
                }
            },
            "swap_events": {
                "counter": "0",
                "guid": {
                    "id": {
                        "addr": "0xbd35135844473187163ca197ca93b2ab014370587bb0ed3befff9e902d6bb541",
                        "creation_num": "204"
                    }
                }
            },
            "timestamp": "1667043934741396",
            "x_reserve": {
                "value": "0"
            },
            "y_reserve": {
                "value": "0"
            }
        }
    }
```

#### 1.3 cetus_amm（10）

```json
  {
    "type": "0xec42a352cc65eca17a9fa85d0fc602295897ed6b8b8af6a6c79ef490eb8f9eba::amm_swap::Pool<0xae478ff7d83ed072dbc5e264250e67ef58f57c99d89b447efd8a0a2e8b2be76e::coin::T, 0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::T>",
    "data": {
      "burn_capability": {
        "dummy_field": false
      },
      "coin_a": {
        "value": "29641"
      },
      "coin_b": {
        "value": "29417780"
      },
      "locked_liquidity": {
        "value": "10"
      },
      "mint_capability": {
        "dummy_field": false
      },
      "protocol_fee_to": "0xec42a352cc65eca17a9fa85d0fc602295897ed6b8b8af6a6c79ef490eb8f9eba"
    }
  }
```

#### 1.4 pancake_swap（11）

```json
  {
    "type": "0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::swap::TokenPairReserve<0x1::aptos_coin::AptosCoin, 0xc7efb4076dbe143cbcd98cfaaa929ecfc8f299203dfff63b95ccb6bfe19850fa::swap::LPToken<0x159df6b7689437016108a019fd5bef736bac692b6d4a1f10c941f6fbb9a74ca6::oft::CakeOFT, 0x1::aptos_coin::AptosCoin>>",
    "data": {
      "block_timestamp_last": "1697192910",
      "reserve_x": "1000102",
      "reserve_y": "10000"
    }
  }
```

#### 1.5 aptoswap （7）

```json
  {
    "type": "0xa5d3ac4d429052674ed38adc62d010e52d7c24ca159194d17ddc196ddb7e480b::pool::Pool<0xae478ff7d83ed072dbc5e264250e67ef58f57c99d89b447efd8a0a2e8b2be76e::coin::T, 0x5e156f1207d0ebfa19a9eeff00d62a282278fb8719f4fab3a586a0a2c0fffbea::coin::T>",
    "data": {
      "admin_fee": "0",
      "connect_fee": "0",
      "fee_direction": 201,
      "freeze": false,
      "incentive_fee": "3",
      "index": "6",
      "ksp_e8_sma": {
        "a0": "572444322880130",
        "a1": "122681531165270",
        "a2": "122685694984653",
        "a3": "163623668635914",
        "a4": "327307972026015",
        "a5": "204620438218280",
        "a6": "122776358751920",
        "c0": "14",
        "c1": "3",
        "c2": "3",
        "c3": "4",
        "c4": "8",
        "c5": "5",
        "c6": "3",
        "current_time": "1733580850",
        "start_time": "1733050788"
      },
      "last_trade_time": "1733580850",
      "liquidity_event": {
        "counter": "120",
        "guid": {
          "id": {
            "addr": "0xa5d3ac4d429052674ed38adc62d010e52d7c24ca159194d17ddc196ddb7e480b",
            "creation_num": "61"
          }
        }
      },
      "lp_fee": "27",
      "lsp_supply": "155423",
      "pool_type": 100,
      "snapshot_event": {
        "counter": "1277",
        "guid": {
          "id": {
            "addr": "0xa5d3ac4d429052674ed38adc62d010e52d7c24ca159194d17ddc196ddb7e480b",
            "creation_num": "62"
          }
        }
      },
      "snapshot_last_capture_time": "1733580096",
      "stable_amp": "0",
      "stable_x_scale": "0",
      "stable_y_scale": "0",
      "swap_token_event": {
        "counter": "2498",
        "guid": {
          "id": {
            "addr": "0xa5d3ac4d429052674ed38adc62d010e52d7c24ca159194d17ddc196ddb7e480b",
            "creation_num": "60"
          }
        }
      },
      "total_trade_24h_last_capture_time": "1733528675",
      "total_trade_x": "10158035",
      "total_trade_x_24h": "112",
      "total_trade_y": "5165297794",
      "total_trade_y_24h": "112607",
      "withdraw_fee": "10",
      "x": {
        "value": "8010"
      },
      "y": {
        "value": "7941020"
      }
    }
  }
```
