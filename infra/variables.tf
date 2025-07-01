variable "project" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  type        = string
  default     = "us-central1"
}

variable "db_user" {
  description = "Postgres username"
  type        = string
  default     = "postgres"
}

variable "db_password" {
  description = "Postgres password"
  type        = string
  sensitive   = true
}

variable "auth0_domain" {
  description = "Auth0 domain"
  type        = string
}

variable "auth0_audience" {
  description = "Auth0 API audience"
  type        = string
}

variable "auth0_client_secret" {
  description = "Auth0 client secret"
  type        = string
  sensitive   = true
}

variable "api_image" {
  description = "Container image for API"
  type        = string
}

variable "ml_image" {
  description = "Container image for ML service"
  type        = string
}

variable "ml_url" {
  description = "URL of ML service"
  type        = string
}