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
            const stockPricesDiv = document.getElementById('stock-prices-chart');
            if (Array.isArray(data) && data.length > 0) {
                // 仅展示最近 20 条记录
                const recentData = data.slice(100, 150).reverse();
                const companyName = recentData[0].company_name; // 获取公司名称

                // 提取日期和股价
                const labels = recentData.map(stock => stock.date);
                const prices = recentData.map(stock => stock.stock_price);

                // 创建图表
                const ctx = document.getElementById('stockChart').getContext('2d');
                const stockChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: companyName+' 股票价格',
                            data: prices,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderWidth: 2.0
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: false
                            }
                        }
                    }
                });

                stockPricesDiv.innerHTML = '股价数据已加载。'; // 更新状态信息
            } else {
                stockPricesDiv.innerHTML = '没有找到股票数据。';
            }
        })
        .catch(error => {
            console.error('Error fetching stock prices:', error);
            document.getElementById('stock-prices-chart').innerHTML = '无法获取股票价格。';
        });
});