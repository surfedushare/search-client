import Axios from 'axios'
import i18n from './i18n'
import store from '~/store'

const baseURL = process.env.VUE_APP_BACKEND_URL + 'api/v1'
const axios = Axios.create({ baseURL })
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'x-csrftoken'

setLanguage(i18n.locale)

axios.interceptors.response.use(
  res => res,
  error => {
    const code = parseInt(error.response && error.response.status)
    if (code === 401) {
      store.dispatch('logout')
    }

    return Promise.reject(error)
  }
)

export function setLanguage(language) {
  axios.defaults.headers.common['Accept-Language'] = language
}

export default axios
