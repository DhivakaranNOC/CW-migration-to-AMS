import boto3
import json

# Initialize the CloudWatch client
client = boto3.client('cloudwatch')

# get current region
session = boto3.Session()
current_region = session.region_name

# Alarm Description for AMS (initial values) with priority as per user input
json_data = {
    "oncall": " ",
    "region": current_region,
    "source": "cloudwatch",
    "Product": "NOC",
    "service": " ",
    "priority": " ",
    "notification_channel": "NOC-testing",
    "alert_owner": "Dhiva"
}

# Define the file containing alarm names
file_name = "alarm.txt"

# Read alarm names from the file
with open(file_name, "r") as file:
    alarm_names = [line.strip() for line in file]

# Function to validate user input for a given range
def get_valid_input(prompt, valid_range):
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            else:
                print("Invalid choice. Please enter a valid option.")
        except ValueError:
            print("Invalid input. Please enter a valid option.")

# Prompt the user for a choice: use default values or specify for each alarm
choice = input("Do you want to set priority as p1 and oncall as yes for all alarms? (yes/no): ").strip().lower()

if choice == "yes":
    # If 'yes', set priority as p0 and oncall as yes for all alarms
    for alarm_name in alarm_names:
        # Define a service mapping dictionary
        service_mapping = {
            0: "AWS/SQS",
            1: "AWS/OpsWorks",
            2: "AWS/RDS",
            3: "AWS/ApplicationELB",
            4: "AWS/NetworkELB",
            5: "AWS/Lambda",
            6: "AWS/ELB",
            7: "AWS/EFS"
        }
        serv = get_valid_input(
            '0. AWS/SQS\n'
            '1. AWS/OpsWorks\n'
            '2. AWS/RDS\n'
            '3. AWS/ApplicationELB\n'
            '4. AWS/NetworkELB\n'
            '5. AWS/Lambda\n'
            '6. AWS/ELB\n'
            '7. AWS/EFS\n'
            f"Select the Service (0, 1, 2, 3, 4, 5, 6 or 7) for alarm {alarm_name}: ",
            range(8)
        )

        # Update the service in the alarm description
        json_data['service'] = f"{service_mapping[serv]}"

        # Update the priority level in the alarm description
        json_data['priority'] = "p0"

        # Update the oncall in the alarm description
        json_data['oncall'] = "no"

        # Add the JSON data to the description
        updated_description = json.dumps(json_data, indent=4)

        # Get the existing alarm details
        response = client.describe_alarms(AlarmNames=[alarm_name])

        # Extract existing alarm metrics
        existing_alarm = response['MetricAlarms'][0]

        # Update the alarm with the modified description
        client.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription=updated_description,
            MetricName=existing_alarm['MetricName'],
            Namespace=existing_alarm['Namespace'],
            Statistic=existing_alarm['Statistic'],
            ComparisonOperator=existing_alarm['ComparisonOperator'],
            Threshold=existing_alarm['Threshold'],
            Period=existing_alarm['Period'],
            EvaluationPeriods=existing_alarm['EvaluationPeriods'],
            TreatMissingData=existing_alarm.get('TreatMissingData', 'default_value'),
            ActionsEnabled=True,
            AlarmActions=[f"arn:aws:sns:{current_region}:018257682911:Ananth-test"],
            OKActions=[f"arn:aws:sns:{current_region}:018257682911:Ananth-test"],
            Dimensions=existing_alarm.get('Dimensions', [])
        )
        print (f"existing_alarm MetricName = '{existing_alarm['MetricName']}")
        print (f"existing_alarm Namespace = '{existing_alarm['Namespace']}")
        print (f"existing_alarm Statistic = '{existing_alarm['Statistic']}")
        print (f"existing_alarm ComparisonOperator = '{existing_alarm['ComparisonOperator']}")
        print (f"existing_alarm EvaluationPeriods = '{existing_alarm['EvaluationPeriods']}")
        print (f"existing_alarm Dimensions = '{existing_alarm.get('TreatMissingData', 'default_value')}")
        print (f"existing_alarm ActionsEnabled = '{existing_alarm['ActionsEnabled']}")
        print (f"existing_alarm Dimensions = '{existing_alarm.get('Dimensions', [])}")

        print (f"Update description for '{alarm_name}' = '{updated_description}")
        print(f"Updated CloudWatch Alarm '{alarm_name}' with priority as p1, oncall as yes, and Service as {service_mapping[serv]}")

else:
    # If 'no', ask for priority, oncall, and service for each alarm
    for alarm_name in alarm_names:
        # Get user input for priority
        priority_mapping = {
            0: "p0",
            1: "p1",
            2: "p2",
            3: "p3"
        }
        pri = get_valid_input(
            '0. p0 (For Immediate Call)\n'
            '1. p1 (Call after 5 mins)\n'
            '2. p2 (Call after 15 mins)\n'
            '3. p3 (Others (Warnings))\n'
            f"Select the priority (0, 1, 2, or 3) for alarm {alarm_name}: ",
            range(4)
        )

        # Get user input for oncall
        oncall_mapping = {
            0: "immediately",
            1: "yes",
            2: "no"
        }
        act = get_valid_input(
            '0. P0 (immediate)\n'
            '1. P1, P2 (yes)\n'
            '2. P3 (no)\n'
            'Select the oncall (0, 1, or 2): ',
            range(3)
        )

        # Define a service mapping dictionary
        service_mapping = {
            0: "AWS/SQS",
            1: "AWS/OpsWorks",
            2: "AWS/RDS",
            3: "AWS/ApplicationELB",
            4: "AWS/NetworkELB",
            5: "AWS/Lambda",
            6: "AWS/ELB",
            7: "AWS/EFS"
        }
        serv = get_valid_input(
            '0. AWS/SQS\n'
            '1. AWS/OpsWorks\n'
            '2. AWS/RDS\n'
            '3. AWS/ApplicationELB\n'
            '4. AWS/NetworkELB\n'
            '5. AWS/Lambda\n'
            '6. AWS/ELB\n'
            '7. AWS/EFS\n'
            f"Select the Service (0, 1, 2, 3, 4, 5, 6 or 7) for alarm {alarm_name}: ",
            range(8)
        )

        # Update the priority level in the alarm description
        json_data['priority'] = f"{priority_mapping[pri]}"

        # Update the oncall in the alarm description
        json_data['oncall'] = f"{oncall_mapping[act]}"

        # Update the service in the alarm description
        json_data['service'] = f"{service_mapping[serv]}"

        # Add the JSON data to the description
        updated_description = json.dumps(json_data, indent=4)

        # Get the existing alarm details
        response = client.describe_alarms(AlarmNames=[alarm_name])

        # Extract existing alarm metrics
        existing_alarm = response['MetricAlarms'][0]

        # Update the alarm with the modified description
        client.put_metric_alarm(
            AlarmName=alarm_name,
            AlarmDescription=updated_description,
            MetricName=existing_alarm['MetricName'],
            Namespace=existing_alarm['Namespace'],
            Statistic=existing_alarm['Statistic'],
            ComparisonOperator=existing_alarm['ComparisonOperator'],
            Threshold=existing_alarm['Threshold'],
            Period=existing_alarm['Period'],
            EvaluationPeriods=existing_alarm['EvaluationPeriods'],
            TreatMissingData=existing_alarm.get('TreatMissingData', 'default_value'),
            ActionsEnabled=True,
            AlarmActions=[f"arn:aws:sns:{current_region}:{priority_mapping[pri]}:018257682911:Ananth-test"],
            OKActions=[f"arn:aws:sns:{current_region}:{priority_mapping[pri]}:018257682911:Ananth-test"],
            Dimensions=existing_alarm.get('Dimensions', [])
        )
    print (f"existing_alarm MetricName = '{existing_alarm['MetricName']}")
    print (f"existing_alarm Namespace = '{existing_alarm['Namespace']}")
    print (f"existing_alarm Statistic = '{existing_alarm['Statistic']}")
    print (f"existing_alarm ComparisonOperator = '{existing_alarm['ComparisonOperator']}")
    print (f"existing_alarm EvaluationPeriods = '{existing_alarm['EvaluationPeriods']}")
    print (f"existing_alarm Dimensions = '{existing_alarm.get('TreatMissingData', 'default_value')}")
    print (f"existing_alarm ActionsEnabled = '{existing_alarm['ActionsEnabled']}")
    print (f"existing_alarm Dimensions = '{existing_alarm.get('Dimensions', [])}")

    print (f"Update description for '{alarm_name}' = '{updated_description}")
    print(f"Updated CloudWatch Alarm '{alarm_name}' with priority as {priority_mapping[pri]} , oncall as {oncall_mapping[act]} , and Service as {service_mapping[serv]}")
