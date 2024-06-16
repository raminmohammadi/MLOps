# Use the official Nginx image from the Docker Hub
FROM nginx:alpine

# Copy custom configuration file if needed (not required for this simple example)
# COPY nginx.conf /etc/nginx/nginx.conf

# Remove the default Nginx HTML file
RUN rm -rf /usr/share/nginx/html/*

# Copy the HTML file to the Nginx server
COPY index.html /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx when the container has provisioned.
CMD ["nginx", "-g", "daemon off;"]
