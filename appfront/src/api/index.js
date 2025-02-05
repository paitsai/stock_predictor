// appfront/src/api/index.js

// 引入 Vue 和 Axios 库
import Vue from 'vue'
import Axios from 'axios'

// 创建一个自定义的 Axios 实例
// 设置 `withCredentials: true` 表示允许跨域请求时携带 cookies（用于身份验证等场景）
const axiosInstance = Axios.create({
    withCredentials: true
})

// 添加请求拦截器
// 每次发送请求之前，都会先执行这里的代码
axiosInstance.interceptors.request.use((config) => {
    // 设置请求头，标明这是一个 AJAX 请求
    config.headers['X-Requested-With'] = 'XMLHttpRequest'

    // 从浏览器的 cookie 中提取 CSRF Token
    // CSRF Token 是一种安全机制，用于防止跨站请求伪造攻击
    const regex = /.*csrftoken=([^;.]*).*$/ // 正则表达式匹配 cookie 中的 csrftoken
    config.headers['X-CSRFToken'] = document.cookie.match(regex) === null ? null : document.cookie.match(regex)[1]

    // 返回修改后的请求配置
    return config
})

// 添加响应拦截器
// 每次接收到响应时，都会先执行这里的代码
axiosInstance.interceptors.response.use(
    // 处理成功的响应
    response => {
        // 直接返回响应数据
        return response
    },
    // 处理错误的响应
    error => {
        // 将错误继续抛出，以便在具体的请求中捕获和处理
        return Promise.reject(error)
    }
)

// 将 axios 实例挂载到 Vue 的原型上
// 这样在 Vue 组件中可以通过 `this.axios` 来访问这个实例
Vue.prototype.axios = axiosInstance

// 导出这个自定义的 axios 实例，以便在其他地方使用
export default axiosInstance