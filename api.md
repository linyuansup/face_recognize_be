# 人脸识别
## /checkFace

参数：

| 参数名 | 含义 | 实例 |
| --- | --- | --- |
| face_id | 128 位识别码，逗号分隔 | -0.11500793,0.06470315,0.04810218,0.06936646,-0.05988635,-0.0287673,-0.06915617,-0.13339332,0.09796929,-0.08543622,0.2615478,-0.04625445,-0.22595935,-0.05097241,-0.10173523,0.13054146,-0.16670188,-0.03788376,-0.03375611,-0.03046174,0.13189165,0.00976594,0.05595458,0.04493563,-0.04195372,-0.34259704,-0.07084784,-0.08632965,0.04919514,-0.0497531,-0.06293356,0.05271393,-0.14633937,-0.03124939,0.00311227,0.03516704,-0.026623,-0.00135698,0.16918682,-0.0080288,-0.18817163,0.03473348,0.04310918,0.21601725,0.18580845,0.12092724,-0.01774834,-0.17783104,0.07017203,-0.18316419,-0.00814144,0.20057246,0.05762993,0.09698086,0.00228008,-0.17083952,0.04215309,0.00440216,-0.06379976,0.04669029,0.04346256,-0.11160605,0.06769672,-0.00374614,0.22946526,0.0290204,-0.10857397,-0.11182286,0.07047864,-0.16085024,-0.09709803,0.06985563,-0.13731907,-0.19230115,-0.32275134,0.01736329,0.43299553,0.10608996,-0.16122976,0.05142213,-0.10820233,-0.02400252,0.15906607,0.17484592,-0.04896756,-0.05809636,-0.1145194,-0.03120369,0.18227682,-0.07144977,-0.04891702,0.23284994,-0.00963755,0.12774237,0.02707931,0.08462292,-0.10782337,0.03119038,-0.08694021,-0.04977069,0.03750266,-0.04660672,0.03910444,0.08995236,-0.16246367,0.07676201,-0.01970413,0.0463319,0.08771611,0.02203613,-0.10264532,-0.04919814,0.09341445,-0.23875618,0.26378065,0.19653007,0.10150975,0.13888544,0.14672713,0.11078589,-0.03392721,-0.00773226,-0.13392447,-0.01976343,0.05105645,0.00536217,0.02576631,-0.0121422
|

返回：

找不到面部信息，则返回 Unknown；找到则返回如下对应的用户信息：

~~~ json
{
  "id": 1,
  "name": "李天阳"
}
~~~

# 添加新用户
## /addUser

参数：
| 参数名 | 含义 | 实例 |
| --- | --- | --- |
| name | 用户名 | 李天阳 |
| isAdmin | 是否为管理员 | false 或 true |
| face_id | 128 位识别码，逗号分隔 | -0.11500793,0.06470315,0.04810218,0.06936646,-0.05988635,-0.0287673,-0.06915617,-0.13339332,0.09796929,-0.08543622,0.2615478,-0.04625445,-0.22595935,-0.05097241,-0.10173523,0.13054146,-0.16670188,-0.03788376,-0.03375611,-0.03046174,0.13189165,0.00976594,0.05595458,0.04493563,-0.04195372,-0.34259704,-0.07084784,-0.08632965,0.04919514,-0.0497531,-0.06293356,0.05271393,-0.14633937,-0.03124939,0.00311227,0.03516704,-0.026623,-0.00135698,0.16918682,-0.0080288,-0.18817163,0.03473348,0.04310918,0.21601725,0.18580845,0.12092724,-0.01774834,-0.17783104,0.07017203,-0.18316419,-0.00814144,0.20057246,0.05762993,0.09698086,0.00228008,-0.17083952,0.04215309,0.00440216,-0.06379976,0.04669029,0.04346256,-0.11160605,0.06769672,-0.00374614,0.22946526,0.0290204,-0.10857397,-0.11182286,0.07047864,-0.16085024,-0.09709803,0.06985563,-0.13731907,-0.19230115,-0.32275134,0.01736329,0.43299553,0.10608996,-0.16122976,0.05142213,-0.10820233,-0.02400252,0.15906607,0.17484592,-0.04896756,-0.05809636,-0.1145194,-0.03120369,0.18227682,-0.07144977,-0.04891702,0.23284994,-0.00963755,0.12774237,0.02707931,0.08462292,-0.10782337,0.03119038,-0.08694021,-0.04977069,0.03750266,-0.04660672,0.03910444,0.08995236,-0.16246367,0.07676201,-0.01970413,0.0463319,0.08771611,0.02203613,-0.10264532,-0.04919814,0.09341445,-0.23875618,0.26378065,0.19653007,0.10150975,0.13888544,0.14672713,0.11078589,-0.03392721,-0.00773226,-0.13392447,-0.01976343,0.05105645,0.00536217,0.02576631,-0.0121422
|

返回：

success 表示注册成功

# 删除用户
## /deleteUser

参数：
| 参数名 | 含义 | 实例 |
| --- | --- | --- |
| id | 用户 ID | 1 |

返回：

找不到该用户则返回 not found，反之则返回 success

# 获取用户列表
## /getAllUser

参数：无

返回：

~~~ json
{
  "users": [
    {
      "face_id": "-0.11500793,0.06470315,0.04810218,0.06936646,-0.05988635,-0.0287673,-0.06915617,-0.13339332,0.09796929,-0.08543622,0.2615478,-0.04625445,-0.22595935,-0.05097241,-0.10173523,0.13054146,-0.16670188,-0.03788376,-0.03375611,-0.03046174,0.13189165,0.00976594,0.05595458,0.04493563,-0.04195372,-0.34259704,-0.07084784,-0.08632965,0.04919514,-0.0497531,-0.06293356,0.05271393,-0.14633937,-0.03124939,0.00311227,0.03516704,-0.026623,-0.00135698,0.16918682,-0.0080288,-0.18817163,0.03473348,0.04310918,0.21601725,0.18580845,0.12092724,-0.01774834,-0.17783104,0.07017203,-0.18316419,-0.00814144,0.20057246,0.05762993,0.09698086,0.00228008,-0.17083952,0.04215309,0.00440216,-0.06379976,0.04669029,0.04346256,-0.11160605,0.06769672,-0.00374614,0.22946526,0.0290204,-0.10857397,-0.11182286,0.07047864,-0.16085024,-0.09709803,0.06985563,-0.13731907,-0.19230115,-0.32275134,0.01736329,0.43299553,0.10608996,-0.16122976,0.05142213,-0.10820233,-0.02400252,0.15906607,0.17484592,-0.04896756,-0.05809636,-0.1145194,-0.03120369,0.18227682,-0.07144977,-0.04891702,0.23284994,-0.00963755,0.12774237,0.02707931,0.08462292,-0.10782337,0.03119038,-0.08694021,-0.04977069,0.03750266,-0.04660672,0.03910444,0.08995236,-0.16246367,0.07676201,-0.01970413,0.0463319,0.08771611,0.02203613,-0.10264532,-0.04919814,0.09341445,-0.23875618,0.26378065,0.19653007,0.10150975,0.13888544,0.14672713,0.11078589,-0.03392721,-0.00773226,-0.13392447,-0.01976343,0.05105645,0.00536217,0.02576631,-0.0121422",
      "id": 1,
      "isAdmin": "true",
      "login_time": [
        "20221021211017"
      ],
      "name": "李天阳"
    },
    {
      "face_id": "太多了不写了，和上面格式一样的",
      "id": 2,
      "isAdmin": "false",
      "login_time": [],
      "name": "李天阳"
    }
  ]
}
~~~

# 更改用户信息
## /changeUserInfo

参数：
| 参数名 | 含义 | 实例 |
| --- | --- | --- |
| id | 用户 ID | 1 |
| name | 用户名 | 李天阳 |
| isAdmin | 是否为管理员 | true |
| face_id | 面部 ID | 太长了不写了 |

返回：

success 表示修改成功，找不到该用户则返回 not found，没有改动则返回 no change

# 获取打卡信息
## /getCheckInInfo

参数：
| 参数名 | 含义 | 实例 |
| --- | --- | --- |
| start_time | 开始时间 | 20221021211017 |
| end_time | 结束时间 | 20221021212017 |

返回：

~~~ json
{
  "李天阳": [
    "2022.10.21 21:10:17",
    "2022.10.21 21:17:53",
    "2022.10.21 21:17:54",
    "2022.10.21 21:17:56"
  ],
    "李天阳": [
    "2022.10.21 21:10:17",
    "2022.10.21 21:17:53",
    "2022.10.21 21:17:54",
    "2022.10.21 21:17:56"
  ]
}
~~~