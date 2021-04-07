storage "file" {
  path = "./vault-data"
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_cert_file = "./certs/localhost.crt"
  tls_key_file = "./certs/localhost.key"
}

ui = true