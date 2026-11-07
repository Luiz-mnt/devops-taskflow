variable "resource_prefix" {
  description = "Prefixo exclusivo do laboratorio ou da execucao efemera; use o mesmo prefixo no Compose da fase 2."
  type        = string
  default     = "taskflow"

  validation {
    condition     = length(var.resource_prefix) <= 40 && can(regex("^[a-z][a-z0-9]*(-[a-z0-9]+)*$", var.resource_prefix))
    error_message = "Use ate 40 caracteres: letras minusculas, numeros e hifens internos, iniciando por letra."
  }
}

variable "docker_host" {
  description = "Endereco opcional do daemon. null usa o padrao do provider/DOCKER_HOST; no Windows pode ser npipe:////./pipe/docker_engine."
  type        = string
  default     = null

  validation {
    condition     = var.docker_host == null ? true : can(regex("^(unix|npipe|ssh|tcp)://.+$", var.docker_host))
    error_message = "Informe um endpoint Docker unix://, npipe://, ssh:// ou tcp://, ou null."
  }
}
