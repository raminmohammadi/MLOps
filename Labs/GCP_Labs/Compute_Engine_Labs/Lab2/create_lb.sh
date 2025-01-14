# Need to get this from your own gcp - follow the video for steps

POST https://compute.googleapis.com/compute/beta/projects/cloud-compute-441619/global/healthChecks
{
  "checkIntervalSec": 5,
  "description": "",
  "healthyThreshold": 2,
  "httpHealthCheck": {
    "host": "",
    "port": 8000,
    "proxyHeader": "NONE",
    "requestPath": "/health"
  },
  "logConfig": {
    "enable": false
  },
  "name": "imdb-health-check",
  "timeoutSec": 5,
  "type": "HTTP",
  "unhealthyThreshold": 2
}

POST https://compute.googleapis.com/compute/v1/projects/cloud-compute-441619/zones/us-central1-a/instanceGroups/imdb-mig/setNamedPorts
{
  "namedPorts": [
    {
      "name": "http",
      "port": 8000
    }
  ]
}

POST https://compute.googleapis.com/compute/beta/projects/cloud-compute-441619/global/backendServices
{
  "backends": [
    {
      "balancingMode": "UTILIZATION",
      "capacityScaler": 1,
      "group": "projects/cloud-compute-441619/zones/us-central1-a/instanceGroups/imdb-mig",
      "maxUtilization": 0.8
    }
  ],
  "cdnPolicy": {
    "cacheKeyPolicy": {
      "includeHost": true,
      "includeProtocol": true,
      "includeQueryString": true
    },
    "cacheMode": "CACHE_ALL_STATIC",
    "clientTtl": 3600,
    "defaultTtl": 3600,
    "maxTtl": 86400,
    "negativeCaching": false,
    "serveWhileStale": 0
  },
  "compressionMode": "DISABLED",
  "connectionDraining": {
    "drainingTimeoutSec": 300
  },
  "description": "",
  "enableCDN": true,
  "healthChecks": [
    "projects/cloud-compute-441619/global/healthChecks/imdb-health-check"
  ],
  "ipAddressSelectionPolicy": "IPV4_ONLY",
  "loadBalancingScheme": "EXTERNAL_MANAGED",
  "localityLbPolicy": "ROUND_ROBIN",
  "logConfig": {
    "enable": false
  },
  "name": "imdb-backend-service",
  "portName": "http",
  "protocol": "HTTP",
  "sessionAffinity": "NONE",
  "timeoutSec": 30
}

POST https://compute.googleapis.com/compute/v1/projects/cloud-compute-441619/global/urlMaps
{
  "defaultService": "projects/cloud-compute-441619/global/backendServices/imdb-backend-service",
  "name": "imdb-lb"
}

POST https://compute.googleapis.com/compute/v1/projects/cloud-compute-441619/global/targetHttpProxies
{
  "name": "imdb-lb-target-proxy",
  "urlMap": "projects/cloud-compute-441619/global/urlMaps/imdb-lb"
}

POST https://compute.googleapis.com/compute/beta/projects/cloud-compute-441619/global/forwardingRules
{
  "IPProtocol": "TCP",
  "ipVersion": "IPV4",
  "loadBalancingScheme": "EXTERNAL_MANAGED",
  "name": "imdb-frontend",
  "networkTier": "PREMIUM",
  "portRange": "80",
  "target": "projects/cloud-compute-441619/global/targetHttpProxies/imdb-lb-target-proxy"
}