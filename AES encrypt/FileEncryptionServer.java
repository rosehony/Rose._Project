import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.*;
import java.net.InetSocketAddress;

public class FileEncryptionServer {

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/encrypt", new EncryptHandler());
        server.createContext("/decrypt", new DecryptHandler());
        server.setExecutor(null);
        server.start();
        System.out.println("Server started on port 8080");
    }

    static class EncryptHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            handleRequest(exchange, "encrypt");
        }
    }

    static class DecryptHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            handleRequest(exchange, "decrypt");
        }
    }

    private static void handleRequest(HttpExchange exchange, String operation) throws IOException {
        InputStream inputStream = exchange.getRequestBody();
        OutputStream outputStream = exchange.getResponseBody();

        String key = exchange.getRequestHeaders().getFirst("key");
        if (key == null) {
            sendResponse(exchange, 400, "Bad Request: Encryption key is missing");
            return;
        }

        try {
            if (operation.equals("encrypt")) {
                FileEncryptionService.encryptFile(inputStream, outputStream, key);
            } else if (operation.equals("decrypt")) {
                FileEncryptionService.decryptFile(inputStream, outputStream, key);
            }

            sendResponse(exchange, 200, "Success");
        } catch (Exception e) {
            e.printStackTrace();
            sendResponse(exchange, 500, "Internal Server Error");
        } finally {
            inputStream.close();
            outputStream.close();
        }
    }

    private static void sendResponse(HttpExchange exchange, int statusCode, String response) throws IOException {
        exchange.sendResponseHeaders(statusCode, response.length());
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}
