output "network_name" {
  description = "Nome da rede externa a ser consumida pelo Compose na fase 2."
  value       = docker_network.taskflow.name
}

output "network_id" {
  description = "Identificador real da rede provisionada."
  value       = docker_network.taskflow.id
}

output "volume_name" {
  description = "Nome do volume externo a ser consumido pelo Compose na fase 2."
  value       = docker_volume.taskflow.name
}

output "volume_id" {
  description = "Identificador real do volume provisionado."
  value       = docker_volume.taskflow.id
}
