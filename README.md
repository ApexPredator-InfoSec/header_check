# header_check
Python script to test for 'Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', and 'Server' headers in a get response

Usage: python3 headers.py -t <target url>
       python3 headers.py -f <file containing urls>
 
Enable debugging thru BRUP or ZAP proxies with -d or --debug
  
This scripts accepts a URL passed with -t or --target and test the URL for the 4 headers listed above.
 ![image](https://user-images.githubusercontent.com/84335647/139359558-8fb35a8a-2eb2-4f28-b93c-5be21766fee6.png)
 
If multiple URLs are needed they can be passed in a file with -f or --file to test all URLs in the file

![image](https://user-images.githubusercontent.com/84335647/139359725-3fcce880-c3f2-4234-8d9f-f279b69b3f4c.png)

