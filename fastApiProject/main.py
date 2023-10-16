import logging

from fastapi import FastAPI
from pydantic import BaseModel, Field

# logging changes
logging.basicConfig(filename=f'/PerfLogs/fastapi_project.log',
                    format='%(asctime)s %(message)s', filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

app = FastAPI()
alert_dict = {}


@app.get("/")
async def root():
    return {"Welcome to Sample FastAPI Project"}


class Alert(BaseModel):
    alert_id: str
    service_id: str = Field(return_in_api=False, exclude=True)
    service_name: str = Field(return_in_api=False, exclude=True)
    model: str
    alert_type: str
    alert_ts: str
    severity: str
    team_slack: str

    def __init__(self, alert_id, service_id, service_name, model, alert_type, alert_ts, severity, team_slack):
        super().__init__(alert_id=alert_id, service_id=service_id, service_name=service_name, model=model,
                         alert_type=alert_type, alert_ts=alert_ts, severity=severity, team_slack=team_slack)


class AlertWriteResponse(BaseModel):
    alert_id: str
    error: str

    def __init__(self, alert_id, error):
        super().__init__(alert_id=alert_id, error=error)


class AlertReadResponse(BaseModel):
    service_id: str
    service_name: str
    alerts: list[Alert] = []

    def __init__(self, service_id, service_name, alerts):
        super().__init__(service_name=service_name, service_id=service_id, alerts=alerts)


@app.post("/alerts", response_model=AlertWriteResponse)
async def alert_post(alert: Alert):
    try:
        alert_dict[alert.alert_id] = alert
        resp = AlertWriteResponse(alert.alert_id, 'Alert Saved Successfully')
    except Exception as ex:
        logger.debug(ex)
        print(ex)
        resp = AlertWriteResponse(alert.alert_id, str(ex))
    return resp


@app.get("/readAlerts", response_model=AlertReadResponse)
async def read_alerts(service_id: str, start_ts: str, end_ts: str):
    alerts = []
    alert: Alert
    service_name = None
    try:
        for alert_id, alert in alert_dict.items():
            if alert.service_id == service_id:
                service_name = alert.service_name
                alerts.append(alert)
    except Exception as ex:
        logger.debug(ex)
        print(ex)
    if service_name is None:
        service_name = "None"
    resp = AlertReadResponse(service_id, service_name, alerts)
    return resp