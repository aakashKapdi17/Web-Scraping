req = Request('https://www.beerwulf.com/en-gb/c/mixedbeercases',headers={
       'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    })


fetch("http://localhost:8050/render.html?url=https://www.beerwulf.com/en-gb/c/mixedbeercases")


beercards:-cards= response.xpath("//div[@id='product-items-container']")
for each card:
        name: cards.xpath("//div[@class='product-title-container']/h4/text()").get()
        price: cards.xpath("//span[@class='price']/text()").get()
    