import random
import pandas as pd
import os

output_dir = 'stock_logs'
os.makedirs(output_dir, exist_ok=True)

# 示例公司名称列表（包含1000个公司名称）
company_names = [
    'Apple Inc.', 'Microsoft Corp.', 'Amazon.com Inc.', 'Alphabet Inc.', 
    'Facebook Inc.', 'Tesla Inc.', 'Berkshire Hathaway Inc.', 'Johnson & Johnson',
    'Visa Inc.', 'Walmart Inc.', 'Procter & Gamble Co.', 'Coca-Cola Co.',
    'PepsiCo Inc.', 'Intel Corp.', 'IBM Corp.', 'Netflix Inc.', 
    'Nike Inc.', 'Adobe Inc.', 'Salesforce.com Inc.', 'Oracle Corp.',
    'Cisco Systems Inc.', 'Qualcomm Inc.', 'Starbucks Corp.', 'Pfizer Inc.',
    'AbbVie Inc.', 'Mastercard Inc.', 'UnitedHealth Group Inc.', '3M Co.',
    'Exxon Mobil Corp.', 'Chevron Corp.', 'Honeywell International Inc.',
    'Bristol-Myers Squibb Co.', 'Bank of America Corp.', 'Goldman Sachs Group Inc.',
    'JPMorgan Chase & Co.', 'American Express Co.', 'Caterpillar Inc.', 
    'General Electric Co.', 'Verizon Communications Inc.', 'AT&T Inc.',
    'T-Mobile US Inc.', 'Lowe’s Companies Inc.', 'Home Depot Inc.',
    'Target Corp.', 'Costco Wholesale Corp.', 'CVS Health Corp.',
    'Kraft Heinz Co.', 'Mondelez International Inc.', 'Walt Disney Co.',
    'IBM Watson Health', 'NVIDIA Corp.', 'PayPal Holdings Inc.', 
    'Salesforce.com Inc.', 'Square Inc.', 'Zoom Video Communications Inc.',
    'Slack Technologies', 'Spotify Technology S.A.', 'Snap Inc.',
    'Pinterest Inc.', 'Twitter Inc.', 'LinkedIn Corp.', 'Yelp Inc.',
    'Shopify Inc.', 'Etsy Inc.', 'Alibaba Group Holding Ltd.',
    'Baidu Inc.', 'Tencent Holdings Ltd.', 'JD.com Inc.',
    'NIO Inc.', 'Li Auto Inc.', 'XPeng Inc.', 'Palantir Technologies',
    'DoorDash Inc.', 'Instacart', 'Robinhood Markets Inc.',
    'Unity Software Inc.', 'CrowdStrike Holdings Inc.', 'Zscaler Inc.',
    'Datadog Inc.', 'Elastic N.V.', 'Fastly Inc.', 'Cloudflare Inc.',
    'RingCentral Inc.', 'Twilio Inc.', 'Shopify Inc.', 'SquareSpace Inc.',
    'Asana Inc.', 'ZoomInfo Technologies Inc.', 'Lucid Motors Inc.',
    'Boeing Co.', 'Lockheed Martin Corp.', 'Northrop Grumman Corp.',
    'Raytheon Technologies Corp.', 'General Dynamics Corp.', 'Textron Inc.',
    '3M Company', 'Honeywell International Inc.', 'Siemens AG',
    'ABB Ltd.', 'Schneider Electric SE', 'Rockwell Automation Inc.',
    'Emerson Electric Co.', 'Eaton Corp.', 'Lennar Corp.',
    'D.R. Horton Inc.', 'PulteGroup Inc.', 'KB Home', 'Toll Brothers Inc.',
    'Kroger Co.', 'Albertsons Companies Inc.', 'Ahold Delhaize',
    'Whole Foods Market', 'Publix Super Markets Inc.', 'H-E-B Grocery Company',
    'Ahold Delhaize USA', 'Metro Inc.', 'Loblaw Companies Ltd.',
    'Best Buy Co. Inc.', 'GameStop Corp.', 'Barnes & Noble Inc.',
    'Bed Bath & Beyond Inc.', 'HomeGoods', 'Marshalls',
    'TJX Companies Inc.', 'Ross Stores Inc.', 'Dollar Tree Inc.',
    'Dollar General Corp.', 'Five Below Inc.', 'Big Lots Inc.',
    'Ollie’s Bargain Outlet', 'Burlington Stores Inc.', 'Macy’s Inc.',
    'Nordstrom Inc.', 'Saks Fifth Avenue', 'Neiman Marcus',
    'J.C. Penney Company Inc.', 'Kohl’s Corp.', 'Sears Holdings Corp.',
    'American Eagle Outfitters Inc.', 'Gap Inc.', 'H&M Hennes & Mauritz AB',
    'Zara', 'Uniqlo', 'L Brands Inc.', 'Victoria’s Secret',
    'Abercrombie & Fitch Co.', 'Express Inc.', 'Forever 21',
    'Lululemon Athletica Inc.', 'Under Armour Inc.', 'Adidas AG',
    'Puma SE', 'New Balance', 'Skechers USA Inc.', 'Reebok',
    'FILA', 'Kappa', 'Champion', 'Hollister Co.',
    'American Apparel', 'Aerie', 'Free People', 'Anthropologie',
    'Urban Outfitters Inc.', 'ModCloth', 'ThredUp Inc.', 'Stitch Fix Inc.',
    'Rent the Runway', 'Poshmark Inc.', 'Depop', 'Grailed',
    'Tradesy', 'The RealReal Inc.', 'Vestiaire Collective',
    'StockX', 'GOAT', 'eBay Inc.', 'Craigslist',
    'Facebook Marketplace', 'OfferUp', 'Letgo', 'Mercari',
    'Poshmark', 'Depop', 'Vinted', 'Carousell',
    'Chairish', '1stdibs', 'Reverb', 'Trove',
    'Sotheby’s', 'Christie’s', 'Heritage Auctions', 'Bonhams',
    'Phillips', 'Catawiki', 'Artfinder', 'Saatchi Art',
    'ArtSpace', 'Artnet', 'Artprice', 'Art Basel',
    'Frieze', 'Sotheby’s Institute of Art', 'Christie’s Education',
    'The Courtauld Institute of Art', 'Goldsmiths, University of London',
    'The Royal Academy of Arts', 'The British Museum',
    'The Museum of Modern Art', 'The Louvre',
    'The Tate Gallery', 'The Metropolitan Museum of Art',
    'The Whitney Museum of American Art', 'The Guggenheim Museum',
    'The Getty Center', 'The National Gallery', 'The National Gallery of Art',
    'The Victoria and Albert Museum', 'The Rijksmuseum',
    'The Van Gogh Museum', 'The State Hermitage Museum',
    'The Uffizi Gallery', 'The Prado Museum', 'The Museo del Prado',
    'The Museo Nacional del Prado', 'The Museo Nacional de Bellas Artes',
    'The Museo de Arte Moderno', 'The Museo de Arte Contemporáneo',
    'The Museo de Bellas Artes', 'The Museo de la Ciudad',
    'The Museo Nacional de Antropología', 'The Museo de Arte Colonial',
    'The Museo de Arte Popular', 'The Museo de Arte Moderno de Medellín',
    'The Museo de Arte de Lima', 'The Museo de Arte de la Universidad de Puerto Rico',
    'The Museo de Arte de Ponce', 'The Museo de Arte de Puerto Rico',
    'The Museo de Arte del Banco de la República', 'The Museo de Arte de Bogotá',
    'The Museo de Arte de la Universidad Nacional de Colombia',
    'The Museo de Arte del Tolima', 'The Museo de Arte de la Isla de Margarita',
    'The Museo de Arte de la Universidad de Los Andes',
    'The Museo de Arte de la Ciudad de México', 'The Museo de Arte de la Ciudad de Quito',
    'The Museo de Arte de la Ciudad de Santo Domingo',
    'The Museo de Arte de la Ciudad de La Habana', 'The Museo de Arte de Santiago de Chile',
    'The Museo de Arte de Buenos Aires', 'The Museo de Arte de Montevideo',
    'The Museo de Arte de Asunción', 'The Museo de Arte de Lima',
    'The Museo de Arte de Caracas', 'The Museo de Arte de Bogotá',
    'The Museo de Arte de La Paz', 'The Museo de Arte de San José',
    'The Museo de Arte de San Salvador', 'The Museo de Arte de Managua',
    'The Museo de Arte de Tegucigalpa', 'The Museo de Arte de Ciudad de Panamá',
    'The Museo de Arte de Santo Domingo', 'The Museo de Arte de Puerto Rico',
    'The Museo de Arte de Mérida', 'The Museo de Arte de Saltillo',
    'The Museo de Arte de Guadalajara', 'The Museo de Arte de León',
    'The Museo de Arte de Querétaro', 'The Museo de Arte de Aguascalientes',
    'The Museo de Arte de Oaxaca', 'The Museo de Arte de Tlaxcala',
    'The Museo de Arte de Zacatecas', 'The Museo de Arte de Durango',
    'The Museo de Arte de San Luis Potosí', 'The Museo de Arte de Baja California',
    'The Museo de Arte de Chiapas', 'The Museo de Arte de Guerrero',
    'The Museo de Arte de Morelos', 'The Museo de Arte de Puebla',
    'The Museo de Arte de Tlaxcala', 'The Museo de Arte de Veracruz',
    'The Museo de Arte de Yucatán', 'The Museo de Arte de Quintana Roo',
    'The Museo de Arte de Campeche', 'The Museo de Arte de Tabasco',
    'The Museo de Arte de Sonora', 'The Museo de Arte de Sinaloa',
    'The Museo de Arte de Nayarit', 'The Museo de Arte de Jalisco',
    'The Museo de Arte de Guanajuato', 'The Museo de Arte de Michoacán',
    'The Museo de Arte de San Luis Potosí', 'The Museo de Arte de Zacatecas',
    'The Museo de Arte de Durango', 'The Museo de Arte de Aguascalientes',
    'The Museo de Arte de Querétaro', 'The Museo de Arte de Estado de México',
    'The Museo de Arte de Puebla', 'The Museo de Arte de Tlaxcala',
    'The Museo de Arte de Veracruz', 'The Museo de Arte de Yucatán',
    'The Museo de Arte de Quintana Roo', 'The Museo de Arte de Campeche',
    'The Museo de Arte de Tabasco', 'The Museo de Arte de Sonora',
    'The Museo de Arte de Sinaloa', 'The Museo de Arte de Nayarit',
    'The Museo de Arte de Jalisco', 'The Museo de Arte de Guanajuato',
    'The Museo de Arte de Michoacán', 'The Museo de Arte de San Luis Potosí',
    'The Museo de Arte de Zacatecas', 'The Museo de Arte de Durango',
    'The Museo de Arte de Aguascalientes', 'The Museo de Arte de Querétaro',
    'The Museo de Arte de Estado de México', 'The Museo de Arte de Puebla',
    'The Museo de Arte de Tlaxcala', 'The Museo de Arte de Veracruz',
    'The Museo de Arte de Yucatán', 'The Museo de Arte de Quintana Roo',
    'The Museo de Arte de Campeche', 'The Museo de Arte de Tabasco',
    'The Museo de Arte de Sonora', 'The Museo de Arte de Sinaloa',
    'The Museo de Arte de Nayarit', 'The Museo de Arte de Jalisco',
    'The Museo de Arte de Guanajuato', 'The Museo de Arte de Michoacán',
    'The Museo de Arte de San Luis Potosí', 'The Museo de Arte de Zacatecas',
    'The Museo de Arte de Durango', 'The Museo de Arte de Aguascalientes',
    'The Museo de Arte de Querétaro', 'The Museo de Arte de Estado de México',
    'The Museo de Arte de Puebla', 'The Museo de Arte de Tlaxcala',
    'The Museo de Arte de Veracruz', 'The Museo de Arte de Yucatán',
    'The Museo de Arte de Quintana Roo', 'The Museo de Arte de Campeche',
    'The Museo de Arte de Tabasco', 'The Museo de Arte de Sonora',
    'The Museo de Arte de Sinaloa', 'The Museo de Arte de Nayarit',
    'The Museo de Arte de Jalisco', 'The Museo de Arte de Guanajuato',
    'The Museo de Arte de Michoacán', 'The Museo de Arte de San Luis Potosí',
    'The Museo de Arte de Zacatecas', 'The Museo de Arte de Durango',
    'The Museo de Arte de Aguascalientes', 'The Museo de Arte de Querétaro',
    'The Museo de Arte de Estado de México', 'The Museo de Arte de Puebla',
    'The Museo de Arte de Tlaxcala', 'The Museo de Arte de Veracruz',
    'The Museo de Arte de Yucatán', 'The Museo de Arte de Quintana Roo',
    'The Museo de Arte de Campeche', 'The Museo de Arte de Tabasco',
    'The Museo de Arte de Sonora', 'The Museo de Arte de Sinaloa',
    'The Museo de Arte de Nayarit', 'The Museo de Arte de Jalisco',
    'The Museo de Arte de Guanajuato', 'The Museo de Arte de Michoacán',
    'The Museo de Arte de San Luis Potosí'
]

# 为了简化示例，这里添加一些占位符
# for i in range(len(company_names)):
#     company_names.append(f"Company {i + len(company_names) + 1}")

def generate_unique_code(country_code, existing_codes):
    while True:
        unique_suffix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
        stock_code = f"{country_code}{unique_suffix}"
        if stock_code not in existing_codes:
            existing_codes.add(stock_code)
            return stock_code

def generate_stock_data(company_name, stock_code, start_date, end_date):
    data = []
    existing_codes = set()
    
    # 生成日期范围
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')
    
    # 随机生成初始股价
    base_price = random.uniform(90, 120)  # 基础股价
    
    for date in date_range:
        # 随机波动范围
        lower_volatility = random.uniform(-10, -1)  # 最小波动
        upper_volatility = random.uniform(1, 10)    # 最大波动
        volatility = random.uniform(lower_volatility, upper_volatility)
        stock_price = round(base_price + volatility, 2)
        if stock_price < 60:
            stock_price = 60+random.uniform(1,3)
        data.append({'Date': date, 'Company Code': stock_code, 'Company Name': company_name, 'Stock Price': stock_price})
        base_price = stock_price
    
    return pd.DataFrame(data)


start_date = '1959-01-01'
end_date = '2030-12-31'

for company_name in company_names:
    country_code = "US"  
    stock_code = generate_unique_code(country_code, set())
    stock_data = generate_stock_data(company_name, stock_code, start_date, end_date)
    
    # 保存到不同的txt文件
    file_name = f"{output_dir}/{company_name.replace(' ', '_')}.csv"  # 将空格替换为下划线
    stock_data.to_csv(file_name, sep='\t', index=False)

print("股票数据已保存到各个公司的txt文件中")