lastPostID = 606

l = range(1,lastPostID+1)

text_file = open("sitemap.xml", "w")

text_file.write('<?xml version="1.0" encoding="UTF-8"?>')
text_file.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd">')
text_file.write('<url><loc>https://www.feedradar.io/</loc><changefreq>hourly</changefreq><priority>1.00</priority></url>')
text_file.write('<url><loc>https://www.feedradar.io/rss</loc><changefreq>hourly</changefreq><priority>1.00</priority></url>')
text_file.write('<url><loc>https://www.feedradar.io/admin/</loc><changefreq>hourly</changefreq><priority>0.85</priority></url>')
text_file.write('<url><loc>https://www.feedradar.io/admin/login.php</loc><changefreq>hourly</changefreq><priority>0.56</priority></url>')
text_file.write('<url><loc>https://www.feedradar.io/admin/modify.php</loc><changefreq>hourly</changefreq><priority>0.85</priority></url>')
text_file.write('<url><loc>https://www.feedradar.io/admin/remove.php</loc><changefreq>hourly</changefreq><priority>0.85</priority></url>')


for i in reversed(l):
	text_file.write('<url><loc>https://www.feedradar.io/redirect.php?postID='+str(i)+'</loc><changefreq>hourly</changefreq><priority>0.85</priority></url>\n')
	text_file.write('<url><loc>https://www.feedradar.io/post.php?postID='+str(i)+'</loc><changefreq>hourly</changefreq><priority>0.85</priority></url>\n')
	
text_file.write('</urlset>');


text_file.close()