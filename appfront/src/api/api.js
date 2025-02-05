/ appfront/src/api/api.js
import axiosInstance from './index'

const axios = axiosInstance

export const getStocks = () => {return axios.get(`http://localhost:8000/api/stocks/`)}

// export const postStocks= (company_code,stock_price,date) => {return axios.post(`http://localhost:8000/api/books/`, {'name': bookName, 'author': bookAuthor})}

export const getStockByCompanyCode = (companyCode) => {
    return axios.get(`http://localhost:8000/api/stocks/${companyCode}/`)
        .then(response => response.data)
        .catch(error => {
            console.error(`Error fetching stock for company code ${companyCode}:`, error);
            throw error; // 重新抛出错误以供后续处理
        });
};