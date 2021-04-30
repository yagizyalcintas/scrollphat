## Requirements:
* Pyhton 3.7
* Pip3 9.0.1 
&nbsp;


## Installation:
1. Clone the repository in a local file.
2. Go into the that directory in terminal and run ``` pip3 install -r requirements.txt ```

&nbsp;






## Image Properties:
* File type: Bmp
* Dimensions: 17x7 Pixels
* bpp: 8

&nbsp;

## How To Create bmp Image:
* **Using GIMP:**
    * ![readme1](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp1.png)&nbsp;
    * ![readme2](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp2.png)&nbsp;
    * ![readme3](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp3.png)&nbsp;
    * ![readme4](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp4.png)&nbsp;
    * ![readme5](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp5.png)&nbsp;
    * ![readme6](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp6.png)&nbsp;
    * ![readme7](https://raw.githubusercontent.com/yagizyalcintas/scrollphat/main/images/gimp7.png)&nbsp;
* **With Hex Editor:**

Refer to this [tutorial](https://medium.com/sysf/bits-to-bitmaps-a-simple-walkthrough-of-bmp-image-format-765dc6857393)

&nbsp;


## Example use:
&nbsp;

* **Uploading Image Using Postman**
&nbsp;

![readme8](https://user-images.githubusercontent.com/47401171/116260656-2b0ab180-a777-11eb-922b-a577c12e2817.png)
![readme9](https://user-images.githubusercontent.com/47401171/116260654-2a721b00-a777-11eb-8bb6-d52b2f05c57d.png)&nbsp;

&nbsp;


* **Uploading Image Using Curl Command**

```
curl --location --request POST 'http://<device ip>:8080/actions/sendImage' --form 'example.bmp=@"<directory of image>/example.bmp"'
```





