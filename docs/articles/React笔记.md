Title: React基础笔记
Date: 2016-04-05 03:43
Author: jmpews
Category: react
Tags: js,react
Slug: react-note

使用react必须要正确的**抽象组件**
### `props`
父组件向子组件传递数据.

### `input`默认值的设置
`defaultValue`仅在load的时候执行一次，不会根据state进行更新。这里可以使用refs来获取到真实dam，然后`this.ref.username.value='test'`
