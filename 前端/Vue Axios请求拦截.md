```js
import Vue from 'vue'
import axios from 'axios'
import qs from 'qs'
import merge from 'lodash/merge'

import {message} from 'element-ui'

const http = axios.create({
  timeout: 1000 * 30,
  withCredentials: true,
  headers: {
      //自定义header  想拼啥就拼啥
    'code': 'r-channel'
  }
})
/**
 * 请求拦截
 */
http.interceptors.request.use(config => {
//TODO 发送请求前要做的事
  return config
}, error => {

  return Promise.reject(error)
})

/**
 * 响应拦截
 */
http.interceptors.response.use(response => {
//TODO 请求完成后要做的事	
  return response
}, error => {
  message({
    showClose:true,
    message:"XXX服务不可用",
    type:'warning',
    duration:3000
  });
  return Promise.reject(error)
})

/**
 * 请求地址处理
 * @param {*} actionName action方法名称
 */
http.adornUrl = (actionName) => {
  // 非生产环境 && 开启代理, 接口前缀统一使用[/proxyApi/]前缀做代理拦截!
  return (process.env.NODE_ENV !== 'production' && process.env.OPEN_PROXY ? '/proxyApi/' : window.SITE_CONFIG.baseUrl) + actionName
}


/**
 * get请求参数处理
 * @param {*} params 参数对象
 * @param {*} openDefultParams 是否开启默认参数?
 */
http.adornParams = (params = {}, openDefultParams = true) => {
  var defaults = {
    't': new Date().getTime(),
  }

  return openDefultParams ? merge(defaults, params) : params
}

/**
 * post请求数据处理
 * @param {*} data 数据对象
 * @param {*} openDefultdata 是否开启默认数据?
 * @param {*} contentType 数据格式
 *  json: 'application/json; charset=utf-8'
 *  form: 'application/x-www-form-urlencoded; charset=utf-8'
 */
http.adornData = (data = {},  contentType = 'form' ,openDefultdata = true) => {
  var defaults = {
    't': new Date().getTime()
  };
  data = openDefultdata ? merge(defaults, data) : data;
  return contentType === 'json' ? JSON.stringify(data) : qs.stringify(data, {indices: false})
};

export default http

```

