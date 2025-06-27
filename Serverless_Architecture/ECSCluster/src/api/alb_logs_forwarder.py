import os
import json
import gzip
import boto3
import traceback
import re
from datetime import datetime
from botocore.exceptions import ClientError, NoCredentialsError
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.logging import correlation_paths

### INIT CONFIGURATIONS --------------------------------------
# ✅ AWS Lambda Powertools Logging, Tracing & Metrics
logger = Logger(service="alb_logs_forwarder", level="INFO")
tracer = Tracer(service="alb_logs_forwarder")
metrics = Metrics(namespace="FargateCluster")

# ✅ AWS Clients
s3 = boto3.client("s3")
logs_client = boto3.client("logs")

### GLOBAL VARIABLES -----------------------------------------
log_group = os.getenv("ALB_LOG_GROUP_NAME", "/ALB/AccessLogs")  
#log_stream = os.getenv("TARGET_LOG_GROUP_NAME", "alb-logs-stream")  
stage = os.getenv("STAGE", "Test")  # Default to "Test" if not set

### HELPER FUNCTION: SEND LOGS TO CLOUDWATCH -----------------
def format_alb_log_stream_name(object_key):
    """
    Converts an ALB log S3 object key into a structured log stream name for CloudWatch Logs.
    
    Expected Input:
      S3 Key: "alb-access-logs/AWSLogs/799960128252/elasticloadbalancing/us-west-2/2025/01/30/my-alb-id_20250130T0955Z_52.42.20.161_3eya5yyt.log.gz"
    Output:
      Log Stream: "app/my-alb-id/2025/01/30/[$LATEST]generated-log-id"
    """
    import re
    match = re.search(r"elasticloadbalancing/.+?/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<alb_id>[^_]+)", object_key)
    if match:
        return f"app/{match.group('alb_id')}/{match.group('year')}/{match.group('month')}/{match.group('day')}/[$LATEST]generated-log-id"
    return "unknown-log-stream"

def send_logs_to_cloudwatch(log_events, object_key):
    log_stream_name = format_alb_log_stream_name(object_key)  # ✅ Generate ALB-style log stream
    try:
        logs_client.create_log_stream(logGroupName=log_group, logStreamName=log_stream_name)
    except logs_client.exceptions.ResourceAlreadyExistsException:
        pass  # Ignore if it already exists

    try:
        logs_client.put_log_events(
            logGroupName=log_group,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
        logger.info(f"📤 Successfully forwarded {len(log_events)} log events to CloudWatch in stream {log_stream_name}.")
    except ClientError as e:
        logger.error(f"❌ AWS ClientError sending logs to CloudWatch: {str(e)}")
    except Exception as err:
        logger.error(f"❌ Unexpected error in CloudWatch log forwarding: {str(err)}")
        logger.debug(traceback.format_exc())

### FUNCTION: PROCESS ALB LOGS --------------------------------
def parse_alb_log_line(log_line):
    """
    Parses an ALB log entry into a structured JSON format.
    """
    fields = log_line.split()
    if len(fields) < 12:  # Basic validation to avoid parsing errors
        logger.warning(f"⚠️ Skipping malformed log entry: {log_line}")
        return None

    return {
        "type": fields[0],  # Example: h2
        "timestamp": fields[1],  # Example: 2025-02-06T13:14:11.060505Z
        "alb_id": fields[2],  # ALB identifier
        "source_ip": fields[3],  # Source IP
        "destination_ip": fields[4],  # Target IP
        "request_processing_time": fields[5],  # Example: 0.001
        "target_processing_time": fields[6],
        "response_processing_time": fields[7],
        "elb_status_code": fields[8],  # HTTP status code
        "target_status_code": fields[9],
        "received_bytes": fields[10],
        "sent_bytes": fields[11],
        "request": fields[12:],  # Remaining data (URI, method, headers, etc.)
    }


def logs_forwarder(event, context):
    """
    Extracts ALB logs from S3, processes them, and forwards them to CloudWatch.
    """
    for record in event["Records"]:
        bucket_name = record["s3"]["bucket"]["name"]
        object_key = record["s3"]["object"]["key"]   # ✅ Extract ALB log filename

        try:
            logger.info(f"📥 Fetching ALB log file from S3: {bucket_name}/{object_key}")

            # ✅ Skip Non-Gzip Files
            if not object_key.endswith(".log.gz"):
                logger.warning(f"⚠️ Skipping non-gzip file: {object_key}")
                continue # Stops processing this iteration, moves to next number

            # ✅ Fetch & Decompress Log File
            response = s3.get_object(Bucket=bucket_name, Key=object_key)
            file_content = response["Body"].read()
            
            try:
                log_data = gzip.decompress(file_content).decode("utf-8")
            except OSError:
                logger.error(f"❌ File is not a valid gzip archive: {object_key}")
                continue

            # ✅ Parse Log Lines
            log_lines = log_data.strip().split("\n")
            if not log_lines:
                logger.warning("⚠️ No log data found in the retrieved file.")
                continue

            # ✅ Format Logs for CloudWatch
            #log_events = [
            #    {"timestamp": int(datetime.utcnow().timestamp() * 1000), "message": line}
            #    for line in log_lines
            #]

            log_events = []
            for line in log_lines:
                structured_log = parse_alb_log_line(line)
                if structured_log:
                    log_events.append({
                        "timestamp": int(datetime.utcnow().timestamp() * 1000),
                        "message": json.dumps(structured_log)  # Convert log entry into JSON
                    })

            logger.info(f"📤 Forwarding {len(log_events)} log events to CloudWatch.")
            send_logs_to_cloudwatch(log_events, object_key)

        except ClientError as e:
            logger.error(f"❌ AWS ClientError while fetching S3 logs: {str(e)}")
        except NoCredentialsError:
            logger.error("❌ AWS credentials not found.")
        except Exception as err:
            logger.error(f"❌ Unexpected error processing ALB logs: {str(err)}")
            logger.debug(traceback.format_exc())

### MAIN LAMBDA HANDLER --------------------------------------
@metrics.log_metrics
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@tracer.capture_lambda_handler
def lambda_handler(event, context: LambdaContext):
    """
    AWS Lambda Entry Point: Processes S3 ALB log events.
    """
    logger.info({"message": "🔍 Received ALB log event", "event_body": event.get("Records", [])})
    
    try:
        logs_forwarder(event, context)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "✅ Logs forwarded successfully"}),
        }
    except ClientError as e:
        logger.error({"message": "❌ AWS ClientError", "error": str(e)})
        return {"statusCode": 500, "body": json.dumps({"error": "AWS service error"})}
    except NoCredentialsError:
        logger.error("❌ AWS credentials missing.")
        return {"statusCode": 500, "body": json.dumps({"error": "AWS credentials error"})}
    except Exception as err:
        logger.error({"message": "❌ Unexpected error", "error": str(err)})
        logger.debug(traceback.format_exc())
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"error": "Unexpected error" if stage == "prod" else str(err)}
            ),
        }