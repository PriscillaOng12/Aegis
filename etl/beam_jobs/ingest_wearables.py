"""Ingest wearable snapshots from Pub/Sub into BigQuery."""

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
    gcloud_options.job_name = 'ingest-wearables'
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as p:
        msgs = (
            p
            | beam.io.ReadFromPubSub(subscription=args.subscription)
            | beam.Map(lambda m: json.loads(m.decode('utf-8')))
        )
        (_
            | 'RawToGCS' >> beam.Map(lambda x: json.dumps(x) + '\n')
            | 'WriteRaw' >> beam.io.WriteToText(
                file_path_prefix=f'gs://{args.raw_bucket}/wearable_snapshots/raw',
                file_name_suffix='.json',
                num_shards=1,
            )
        )
        (_
            | 'RowForBQ' >> beam.Map(lambda x: {
                'id': x.get('id'),
                'user_id': x.get('user_id'),
                'source': x.get('source'),
                'timestamp': x.get('timestamp'),
                'hr': x.get('hr'),
                'hrv': x.get('hrv'),
                'steps': x.get('steps'),
                'sleep': x.get('sleep'),
                'created_at': x.get('created_at'),
            })
            | 'WriteBQ' >> beam.io.WriteToBigQuery(
                table=args.output_table,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            )
        )


if __name__ == '__main__':
    run()