# Prometheus/Grafana Monitoring

## Overview

CloudForge uses Prometheus and Grafana for comprehensive monitoring and alerting. The monitoring stack is configured to track application metrics, system resources, and infrastructure health.

## Prometheus Configuration

### prometheus.yml

```yaml
# cloudforge/monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'cloudforge-gateway'
    static_configs:
      - targets: ['cloudforge-gateway:8000']
    metrics_path: '/api/v1/metrics'
    follow_redirects: true

  - job_name: 'cloudforge-catalog'
    static_configs:
      - targets: ['cloudforge-catalog:8001']
    metrics_path: '/metrics'
    follow_redirects: true

  - job_name: 'cloudforge-orders'
    static_configs:
      - targets: ['cloudforge-orders:8002']
    metrics_path: '/metrics'
    follow_redirects: true

  - job_name: 'kubernetes-nodes'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - source_labels: [__meta_kubernetes_node_name]
        target_labels: [instance]

  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_scrape]
        target_labels: [prometheus_scrape]
      - source_labels: [__meta_kubernetes_pod_name]
        target_labels: [pod_name]
```
