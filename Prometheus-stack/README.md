Deploy stack:
# helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
# helm install promstack \
--create-namespace \
--namespace monitoring \
prometheus-community/kube-prometheus-stack --version 52.1.0 (version is optional)

Ensure pod are ready:
# kubectl -n monitoring  get pods

Additional info on https://spacelift.io/blog/prometheus-kubernetes
Access to grafana with ‘prom-operator’ password

Create secret for telegram bot token:
# kubectl create secret generic telegram-bot-token \
--from-literal=token='<YOUR_TELEGRAM_BOT_TOKEN>' \
--namespace monitoring

Create AlertmanagerConfig:

# cat << EOF > alertmanagerconfig.yaml
apiVersion: monitoring.coreos.com/v1alpha1
kind: AlertmanagerConfig
metadata:
  name: telegram-receiver-config
  namespace: monitoring # Must be the same namespace as your Alertmanager
  labels:
    alertmanagerConfig: enabled
spec:
  receivers:
    - name: 'telegram-receiver'
      telegramConfigs:
        - chatID: <YOUR_TELEGRAM_CHAT_ID>
          sendResolved: true
          # Reference the secret created in Step 2
          botToken:
            name: telegram-bot-token
            key: token
  route:
    groupBy: ['alertname', 'cluster', 'severity']
    groupWait: 30s
    groupInterval: 5m
    repeatInterval: 4h
    receiver: 'telegram-receiver'
EOF

Add the following lines to values.yaml (this ensures that telegram will receive all alerts):

alertmanager:
  alertmanagerSpec:
    alertmanagerConfigMatcherStrategy:
      type: None

Upgrade helm chart:
helm upgrade promstack --namespace monitoring prometheus-community/kube-prometheus-stack --version 52.1.0 -f values.yaml

More info on at: https://dev.to/alimehr75/alertmanager-with-telegram-for-prometheus-stack-in-k8s-2n5p

If after deploying prometheus stack, we keep getting alert like, “KubeProxy is down”, go to kube-proxy config map and change from “metricsBindAddress: 127.0.0.1:1024” to “metricsBindAddress: 0.0.0.0:10249”

We can also change telegram alert template:

alertmanager:
  alertmanagerSpec:
    alertmanagerConfigMatcherStrategy:
      type: None
  templateFiles:
    telegram.tmpl: |-
      {{ define "telegram.default.message" }}
      Alert: <b>{{ .CommonLabels.alertname }}</b>

      Status: {{ if eq .Status "firing" }}🔥 <b>FIRING</b>{{ else }}✅ <b>RESOLVED</b>{{ end }}
      Severity: {{ .CommonLabels.severity | title }}

      <b>Description:</b>
      {{ range .Alerts }}
      {{ .Annotations.description }}
      {{ end }}
      {{ end }}

Again, upgrade helm revision
