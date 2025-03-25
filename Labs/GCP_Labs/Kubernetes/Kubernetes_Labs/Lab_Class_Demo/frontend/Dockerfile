# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Remove the default Nginx HTML files
RUN rm -rf /usr/share/nginx/html/*

# Copy HTML files to the Nginx directory
COPY index.html /usr/share/nginx/html
COPY favicon.ico /usr/share/nginx/html

# Copy the custom nginx.conf file to the nginx configuration directory
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Start Nginx when the container has provisioned
CMD ["nginx", "-g", "daemon off;"]

