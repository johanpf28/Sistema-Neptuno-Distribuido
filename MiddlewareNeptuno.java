import java.io.*;
import java.net.*;
import java.sql.*;

public class MiddlewareNeptuno {

    private static final String URL = "jdbc:mysql://localhost:3306/neptuno";
    private static final String USER = "appuser";
    private static final String PASS = "123456";

    public static void main(String[] args) {
        int puerto = 5000;

        try (ServerSocket serverSocket = new ServerSocket(puerto)) {
            System.out.println(">>> Middleware Java iniciado en el puerto " + puerto);
            System.out.println(">>> Esperando conexión del cliente Python...");

            while (true) {
                try (Socket clientSocket = serverSocket.accept();
                     DataInputStream entrada = new DataInputStream(clientSocket.getInputStream());
                     DataOutputStream salida = new DataOutputStream(clientSocket.getOutputStream())) {

                    System.out.println("\n[Cliente conectado desde: " + clientSocket.getInetAddress() + "]");

                   
                    String opcion = entrada.readUTF();

                    if (opcion.equals("REGISTRAR_PRODUCTO")) {
                        String nombre = entrada.readUTF();
                        double precio = entrada.readDouble();
                        int stock = entrada.readInt();
                        
                        String resultado = registrarProducto(nombre, precio, stock);
                        salida.writeUTF(resultado);

                    } else if (opcion.equals("REALIZAR_PEDIDO")) {
                        int idProducto = entrada.readInt();
                        int cantidad = entrada.readInt();
                        
                        String resultado = procesarPedidoAtomico(idProducto, cantidad);
                        salida.writeUTF(resultado);
                    }

                } catch (Exception e) {
                    System.out.println("Error procesando petición: " + e.getMessage());
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

  
    private static String registrarProducto(String nombre, double precio, int stock) {
        String query = "INSERT INTO productos (NombreProducto, PrecioUnidad, UnidadesEnExistencia) VALUES (?, ?, ?)";
        try (Connection conn = DriverManager.getConnection(URL, USER, PASS);
             PreparedStatement ps = conn.prepareStatement(query)) {
            
            ps.setString(1, nombre);
            ps.setDouble(2, precio);
            ps.setInt(3, stock);
            ps.executeUpdate();
            return "OK: Producto registrado con éxito.";
            
        } catch (SQLException e) {
            return "ERROR DB: " + e.getMessage();
        }
    }

    
        private static String procesarPedidoAtomico(int idProd, int cantidad) {
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(URL, USER, PASS);
           
            conn.setAutoCommit(false);

          
            String sqlStock = "SELECT UnidadesEnExistencia FROM productos WHERE idProducto = ?";
            PreparedStatement psStock = conn.prepareStatement(sqlStock);
            psStock.setInt(1, idProd);
            ResultSet rs = psStock.executeQuery();

            if (rs.next()) {
                int stockActual = rs.getInt("UnidadesEnExistencia");

                if (stockActual >= cantidad) {
              
                    String sqlUpdate = "UPDATE productos SET UnidadesEnExistencia = UnidadesEnExistencia - ? WHERE idProducto = ?";
                    PreparedStatement psUpdate = conn.prepareStatement(sqlUpdate);
                    psUpdate.setInt(1, cantidad);
                    psUpdate.setInt(2, idProd);
                    psUpdate.executeUpdate();

                   
                    conn.commit();
                    return "OK: Pedido procesado. Stock actualizado.";
                } else {
                    return "ERROR: Stock insuficiente (Disponible: " + stockActual + ")";
                }
            } else {
                return "ERROR: El producto no existe.";
            }

        } catch (SQLException e) {
            if (conn != null) {
                try { conn.rollback(); } catch (SQLException ex) { ex.printStackTrace(); }
            }
            return "ERROR TRANSACCIÓN: " + e.getMessage();
        } finally {
            if (conn != null) {
                try { conn.close(); } catch (SQLException e) { e.printStackTrace(); }
            }
        }
    }
}