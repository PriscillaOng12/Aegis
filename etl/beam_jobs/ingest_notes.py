"""Apache Beam pipeline for ingesting symptom notes from Pub/Sub.

This pipeline reads JSON messages from a Pub/Sub subscription, writes raw
payloads to GCS for archival and inserts records into BigQuery with a
schema defined in `etl/infra/schemas/symptom_logs.json`.
"""

import argparse
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--subscription', required=True)
    parser.add_argument('--output_table', required=True)
    parser.add_argument('--raw_bucket', required=True)
    args, beam_args = parser.parse_known_args(argv)

    options = PipelineOptions(beam_args)
    gcloud_options = options.view_as(GoogleCloudOptions)
    gcloud_options.project = args.project
    gcloud_options.job_name = 'ingest-notes'
    options.view_as(StandardOptions).streaming = True

    def parse_message(msg):
        payload = json.loads(msg.decode('utf-8'))
        return payload

    with beam.Pipeline(options=options) as p:
        messages = (
            p
            | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(subscription=args.subscription, with_attributes=False)
            | 'ParseJSON' >> beam.Map(parse_message)
        )
        # Write raw messages to GCS
        (_
            | 'FormatForGCS' >> beam.Map(lambda x: json.dumps(x) + '\n')
            | 'WriteRawToGCS' >> beam.io.WriteToText(
                file_path_prefix=f'gs://{args.raw_bucket}/symptom_logs/raw',
                file_name_suffix='.json',
                num_shards=1,
            )
        )
        # Write structured rows to BigQuery
        (_
            | 'ToBigQueryRow' >> beam.Map(lambda x: {
                'id': x.get('id'),
                'user_id': x.get('user_id'),
                'pain': x.get('pain'),
                'fatigue': x.get('fatigue'),
                'nausea': x.get('nausea'),
                'notes': x.get('notes'),
                'timestamp': x.get('timestamp'),
                'created_at': x.get('created_at'),
            })
            | 'WriteToBigQuery' >> beam.io.WriteToBigQuery(
                table=args.output_table,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == '__main__':
    run()