terraform {
  required_version = ">= 1.3.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 5.0.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

module "network" {
  source  = "terraform-google-modules/network/google"
  version = "5.1.0"
  project_id   = var.project
  network_name = "aegis-network"
  subnets = [
    {
      subnet_name   = "aegis-subnet"
      subnet_ip     = "10.10.0.0/16"
      subnet_region = var.region
    }
  ]
}

module "cloud_sql" {
  source  = "terraform-google-modules/sql-db/google//modules/postgresql"
  version = "10.0.0"
  project_id  = var.project
  name        = "aegis-postgres"
  region      = var.region
  database_version = "POSTGRES_14"
  tier        = "db-custom-2-7680"
  disk_size   = 20
  user_name   = var.db_user
  user_password = var.db_password
  ipv4_enabled = false
  deletion_protection = false
}

resource "google_secret_manager_secret" "auth0_client_secret" {
  secret_id = "auth0-client-secret"
  replication { automatic = true }
}

resource "google_secret_manager_secret_version" "auth0_client_secret_version" {
  secret      = google_secret_manager_secret.auth0_client_secret.id
  secret_data = var.auth0_client_secret
}

module "pubsub" {
  source  = "terraform-google-modules/pubsub/google"
  version = "3.1.0"
  project_id = var.project
  topic_name = "aegis-events"
  subscriptions = [
    {
      name  = "symptom-notes-sub"
      ack_deadline_seconds = 30
    },
    {
      name  = "wearable-snapshots-sub"
      ack_deadline_seconds = 30
    }
  ]
}

resource "google_bigquery_dataset" "aegis_dataset" {
  dataset_id = "aegis"
  location   = var.region
}

resource "google_bigquery_table" "features" {
  table_id   = "features"
  dataset_id = google_bigquery_dataset.aegis_dataset.dataset_id
  schema     = file("${path.module}/../etl/infra/schemas/features.json")
  deletion_protection = false
  time_partitioning {
    type = "DAY"
    field = "day"
  }
}

resource "google_cloud_run_service" "api" {
  name     = "aegis-api"
  location = var.region

  template {
    spec {
      containers {
        image = var.api_image
        env = [
          {
            name  = "DATABASE_URL"
            value = "postgresql+asyncpg://${module.cloud_sql.instance_connection_name}/aegis?user=${var.db_user}&password=${var.db_password}"
          },
          {
            name  = "ML_SERVICE_URL"
            value = var.ml_url
          },
          {
            name  = "AUTH0_DOMAIN"
            value = var.auth0_domain
          },
          {
            name  = "AUTH0_AUDIENCE"
            value = var.auth0_audience
          }
        ]
      }
    }
  }

  traffics {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service" "ml" {
  name     = "aegis-ml"
  location = var.region
  template {
    spec {
      containers {
        image = var.ml_image
      }
    }
  }
  traffics {
    percent         = 100
    latest_revision = true
  }
}