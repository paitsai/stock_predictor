// 调用api接口的地址需要自己按需修改

document.addEventListener('DOMContentLoaded', function() {
    const companyCode = 'US1CNFS'; // 示例公司的股票代码
    const url = `http://127.0.0.1:8000/api/get_stocks_prices_by_code/${companyCode}/`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            const stockPricesDiv = document.getElementById('stock-prices');
            // 创建表格
            let tableHtml = '<table><tr><th>公司代码</th><th>公司名称</th><th>日期</th><th>股票价格</th></tr>';
              const recentData = data.slice(100, 108);
              recentData.forEach(stock => {
                tableHtml += `<tr>
                  <td>${stock.company_code}</td>
                    <td>${stock.company_name}</td>  
                    <td>${stock.date}</td>
                    <td>${stock.stock_price}</td>
                </tr>`;
            });
            tableHtml += '</table>';
            stockPricesDiv.innerHTML = tableHtml; // 将表格添加到页面
        })
        .catch(error => {
            console.error('Error fetching stock prices:', error);
            document.getElementById('stock-prices').innerHTML = '无法获取股票价格';
        });
});