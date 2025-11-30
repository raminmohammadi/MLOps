docker build -t dockerfile:v1 .

docker save dockerfile:v1 > my_image.tar

docker run dockerfile:v1
