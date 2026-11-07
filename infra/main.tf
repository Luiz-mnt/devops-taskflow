provider "docker" {
  host = var.docker_host
}

# Terraform e o unico proprietario da rede e do volume.
# Na fase 2, o Compose devera referencia-los como external: true.
resource "docker_network" "taskflow" {
  name   = "${var.resource_prefix}-net"
  driver = "bridge"

  labels {
    label = "com.taskflow.managed-by"
    value = "terraform"
  }

  labels {
    label = "com.taskflow.environment"
    value = var.resource_prefix
  }
}

resource "docker_volume" "taskflow" {
  name   = "${var.resource_prefix}-data"
  driver = "local"

  labels {
    label = "com.taskflow.managed-by"
    value = "terraform"
  }

  labels {
    label = "com.taskflow.environment"
    value = var.resource_prefix
  }
}
