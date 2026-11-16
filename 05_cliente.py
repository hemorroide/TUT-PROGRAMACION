import socket

class Instrumento:
    def __init__(self, host="127.0.0.1", puerto=5555):
        # Creamos el socket y nos conectamos al puerto del instrumento virtual
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, puerto))
        # Creamos un archivo lógico de lectura/escritura para operar por líneas
        self.conexion = self.s.makefile("rw", encoding="utf-8")

    def enviar(self, comando):
        """Manda una orden y no espera respuesta."""
        self.conexion.write(comando + "\n")
        self.conexion.flush()

    def preguntar(self, comando):
        """Manda una consulta y devuelve la respuesta del instrumento."""
        self.enviar(comando)
        respuesta = self.conexion.readline()
        return respuesta.strip()

    def cerrar(self):
        """Cierra la conexión."""
        self.conexion.close()
        self.s.close()

# --- Pruebas del Ejercicio 5 ---
if __name__ == "__main__":
    # OJO: Para correr esta prueba, el instrumento virtual (instrumento_virtual.py) 
    # tiene que estar corriendo en otra terminal en el puerto 5555.
    try:
        inst = Instrumento("127.0.0.1", 5555)
        
        # Prueba mínima pedida por la cátedra
        resp = inst.preguntar("*IDN?")
        assert resp == "OWON,ADS3202,25470803,V1.2.0"
        
        inst.cerrar()
        print("¡Pruebas del Ejercicio 5 OK!")
    except ConnectionRefusedError:
        print("AVISO: No se pudo conectar al instrumento virtual. Acuérdate de correr 'python3 instrumento_virtual.py' en otra terminal.")