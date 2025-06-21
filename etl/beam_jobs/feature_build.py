"""Beam job to build aggregated features for model training and inference.

This job reads symptom logs and wearable snapshots from BigQuery, computes
rolling statistics (e.g. mean HRV over 3 days), and writes the feature
vectors into a feature table.
"""

import argparse
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions


def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', required=True)
    parser.add_argument('--logs_table', required=True)
    parser.add_argument('--wearables_table', required=True)
    parser.add_argument('--feature_table', required=True)
    args, beam_args = parser.parse_known_args(argv)

    options = PipelineOptions(beam_args)
    gcloud_options = options.view_as(GoogleCloudOptions)
    gcloud_options.project = args.project
    gcloud_options.job_name = 'build-features'

    with beam.Pipeline(options=options) as p:
        # Read logs and wearables from BigQuery; this example uses simplified
        # queries. In production, use parameterised queries and windowing.
        logs = (
            p
            | 'ReadLogs' >> beam.io.Read(beam.io.BigQuerySource(query=f'SELECT user_id, pain, fatigue, nausea, TIMESTAMP_TRUNC(timestamp, DAY) as day FROM `{args.logs_table}`'))
        )
        wearables = (
            p
            | 'ReadWearables' >> beam.io.Read(beam.io.BigQuerySource(query=f'SELECT user_id, hr, hrv, steps, sleep, TIMESTAMP_TRUNC(timestamp, DAY) as day FROM `{args.wearables_table}`'))
        )

        # Join logs and wearables by user_id and day
        keyed_logs = logs | 'KeyLogs' >> beam.Map(lambda x: ((x['user_id'], x['day']), x))
        keyed_wear = wearables | 'KeyWear' >> beam.Map(lambda x: ((x['user_id'], x['day']), x))

        joined = ({'logs': keyed_logs, 'wearables': keyed_wear}) | 'CoGroup' >> beam.CoGroupByKey()

        def compute_features(element):
            (user_id, day), groups = element
            logs_list = groups['logs']
            wear_list = groups['wearables']
            # Aggregate wearables
            hr_mean = sum(w['hr'] or 0 for w in wear_list) / max(len(wear_list), 1)
            hrv_mean = sum(w['hrv'] or 0 for w in wear_list) / max(len(wear_list), 1)
            steps_sum = sum(w['steps'] or 0 for w in wear_list)
            sleep_efficiency = sum(w['sleep'] or 0 for w in wear_list) / 480.0  # assume 8h ideal
            # Latest symptom (take max levels)
            pain = max((l['pain'] for l in logs_list), default=0)
            fatigue = max((l['fatigue'] for l in logs_list), default=0)
            nausea = max((l['nausea'] for l in logs_list), default=0)
            return {
                'user_id': user_id[0],
                'day': str(day),
                'pain': pain,
                'fatigue': fatigue,
                'nausea': nausea,
                'hr_mean_1d': hr_mean,
                'hrv_rmssd_mean_3d': hrv_mean,  # placeholder, not true rolling window
                'sleep_efficiency_mean_7d': sleep_efficiency,  # placeholder
                'steps_sum_1d': steps_sum,
            }

        features = joined | 'Compute' >> beam.Map(compute_features)
        features | 'WriteFeatures' >> beam.io.WriteToBigQuery(
            args.feature_table,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        )


if __name__ == '__main__':
    run()