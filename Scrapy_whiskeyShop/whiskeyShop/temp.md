 products=response.css('div.product-item-info')
Name:  products.css('a.product-item-link::text').get() 
price: products.css('span.price::text').get() 
link:- products.css('a.product.photo.product-item-photo').attrib['href'] 
next page:-response.css('a.action.next').attrib['href'] 